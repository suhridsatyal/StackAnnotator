from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from annotator.models import Annotation, Video, Task
from annotator.serializers import AnnotationSerializer, TaskSerializer, VideoSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import APIException
from requests_oauthlib import OAuth1
from django.conf import settings
import requests
import time
import json
import re

POST_STATUS_TWITTER_URL = "https://api.twitter.com/1.1/statuses/update.json"

# our app key and secret we get from the twitter app site
CONSUMER_KEY = settings.SA_CONSUMER_KEY
CONSUMER_SECRET = settings.SA_CONSUMER_SECRET

# get the below through calling API
ACCESS_TOKEN = settings.SA_ACCESS_TOKEN
ACCESS_TOKEN_SECRET = settings.SA_ACCESS_TOKEN_SECRET


def index(request):
    return render(request, 'index.html')


class AnnotationListView(generics.ListCreateAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer
    paginate_by = 50

    def get_queryset(self, **kwargs):
        queryset = Annotation.objects.all()
        question_id = self.request.query_params.get('question_id', None)
        answer_id = self.request.query_params.get('answer_id', None)
        try:
            if question_id:
                queryset = queryset.filter(question_id=int(question_id))
            if answer_id:
                queryset = queryset.filter(answer_id=int(answer_id))
        except ValueError:
            raise Http404
        return queryset


class AnnotationView(generics.RetrieveAPIView):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer


class VideoListView(generics.ListCreateAPIView):
    model = Video
    serializer_class = VideoSerializer
    paginate_by = 50

    def get_queryset(self, **kwargs):
        queryset = Video.objects.all()
        annotation_id = self.request.query_params.get('annotation_id', None)
        try:
            if annotation_id:
                queryset = queryset.filter(annotation_id_id=int(annotation_id))
        except ValueError:
            raise Http404
        return queryset


class VideoView(generics.RetrieveUpdateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class TaskView(APIView):
    def create_message(self, keyword, url):
        # TODO: craft effective tweet

        tweet = "Help me find videos for %s at %s #stackannotator" % \
        (keyword, url)

        return tweet


    def post(self, request, format=None):
        if 'question_id' not in request.POST \
            or 'answer_id' not in request.POST \
           or 'keyword' not in request.POST:

            errorMsg = {
                'Error': "Input Error",
                'Message': "Missing fields (add something better)"
            }
            return Response(errorMsg, status=status.HTTP_400_BAD_REQUEST)

        message = self.create_message(request.POST.get('keyword'),
                                      request.POST.get('annotation_url'))

        auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,
                        ACCESS_TOKEN_SECRET)

        post_res = requests.post(POST_STATUS_TWITTER_URL,
                                    data={'status': message}, auth=auth)

        tweet_info = post_res.json()

        if 'id' not in tweet_info:
            errorMsg = {
                'Error': "Twitter Error",
                'Twitter Response': tweet_info.pop('errors')
            }
            return Response(errorMsg, status=status.HTTP_400_BAD_REQUEST)

        # create a new annotation with data
        newAnnotation = Annotation()
        newAnnotation.question_id = request.POST.get('question_id')
        newAnnotation.answer_id = request.POST.get('answer_id')
        newAnnotation.keyword = request.POST.get('keyword')

        newAnnotation.save()

        task = Task()
        task.tweet_id = tweet_info['id']
        task.annotation_id = newAnnotation.id
        task.created_on = time.strftime('%Y-%m-%d %H:%M:%S',
                            time.strptime(tweet_info['created_at'],
                            '%a %b %d %H:%M:%S +0000 %Y'))
        task.checked_on = time.strftime('%Y-%m-%d %H:%M:%S',
                            time.strptime(tweet_info['created_at'],
                            '%a %b %d %H:%M:%S +0000 %Y'))

        task.save()

        return Response(TaskSerializer(task).data,
                        status=status.HTTP_201_CREATED)


    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404


    def get(self, request, pk=None, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)


class TaskListView(generics.ListAPIView):
    model = Task
    serializer_class = TaskSerializer
    paginate_by = 50

    def get_queryset(self, **kwargs):
        return Task.objects.all()
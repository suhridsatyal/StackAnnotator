from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import time
import json

# from django import forms
# from django.views.generic import DetailView
# from django.views.generic.edit import FormMixin

from annotator.models import Annotation, Video, Task, TaskCreate
from annotator.serializers import AnnotationSerializer, VideoSerializer, TaskSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import APIException

from twitter_aux import tweeter

import re


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
    """
    Retrieve, update or delete a snippet instance.
    """
    def post(self, request, format=None):            
        if 'question_id' not in request.POST or 'answer_id' not in request.POST or 'keyword' not in request.POST or 'position' not in request.POST:
            errorMsg = {
                'Error': "Input Error",
                'Message': "Missing fields (add something better)"
            }
            return Response(errorMsg, status=status.HTTP_400_BAD_REQUEST)

        # tweet and get id
        tweetInfo = tweeter.send_tweet("Help me find videos for " + request.POST.get('keyword') + "#stackannotator")
        
        if 'id' not in tweetInfo:
            errorMsg = {
                'Error': "Twitter Error",
                'Twitter Response': tweetInfo.pop('errors')
            }
            
            return Response(errorMsg, status=status.HTTP_400_BAD_REQUEST)

        # create a new annotation with data
        newAnnotation = Annotation()
        newAnnotation.question_id = request.POST.get('question_id')
        newAnnotation.answer_id = request.POST.get('answer_id')
        newAnnotation.keyword = request.POST.get('keyword')
        newAnnotation.position = request.POST.get('position')
        
        newAnnotation.save()

        task = Task()
        task.tweet_id = tweetInfo['id']
        task.annotation_id = newAnnotation.id
        task.created_on = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweetInfo['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        task.checked_on = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweetInfo['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
 
        task.save()

        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskListView(generics.ListAPIView):
    model = Task
    serializer_class = TaskSerializer
    paginate_by = 50

    def get_queryset(self, **kwargs):
        queryset = Task.objects.all()
        
        return queryset









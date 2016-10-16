from annotator.models import Annotation, Video, Task
from annotator.serializers import AnnotationSerializer, TaskSerializer, VideoSerializer
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from requests_oauthlib import OAuth1
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import json
import re
import requests

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


    def post(self, request, format=None):

        # Remember video data if a video needs to be created
        request.POST._mutable = True

        video_data = request.data.get('videos', None)
        print(video_data)
        videos = None

        if video_data:
            videos = video_data

        request.data["videos"] = []

        # Create annotation
        serializer = AnnotationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        # Create video/videos
        if videos:
            annotation_id = int(serializer.data['id'])
            # Can create multiple videos, may not be required
            for video in videos:
                external_id = video["external_id"]
                # Check if there is a start time
                if "start_time" in video:
                    start_time = video["start_time"]
                    new_video = {"annotation_id": annotation_id,
                                 "external_id": external_id,
                                 "start_time": start_time}
                else:
                    new_video = {"annotation_id": annotation_id,
                                 "external_id": external_id}

                videos = VideoSerializer(data=new_video)
                if videos.is_valid():
                    videos.save()
                else:
                    return Response(videos.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
        # Since it's a post, the data inside shouldn't matter too much
        # Will need to call get to return the correct data
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnnotationView(generics.RetrieveUpdateAPIView):
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


    def post(self, request, format=None):

        serializer = VideoSerializer(data=request.data)

        # Create Video
        if serializer.is_valid():
            # Check if there is a duplicate
            duplicate = Video.objects.all()
            external_id = request.data['external_id']
            annotation_id = request.data['annotation_id']
            duplicate = duplicate.filter(external_id=external_id)
            duplicate = duplicate.filter(annotation_id=annotation_id)
            # If no duplicate then save
            if not duplicate.exists():
                serializer.save()
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VideoView(generics.RetrieveUpdateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


@api_view(['POST'])
def upvote_video(request, pk):
    try:
        video = Video.objects.get(pk=pk)
        video.upvotes = video.upvotes + 1
        video.save()
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def downvote_video(request, pk):
    try:
        video = Video.objects.get(pk=pk)
        video.downvotes = video.downvotes + 1
        video.save()
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def flag_video(request, pk):
    try:
        video = Video.objects.get(pk=pk)
        video.flags = video.flags + 1
        video.save()
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskListView(APIView):
    TASK_TYPE_DETAILS = 0
    TASK_TYPE_TUTORIAL = 1
    TASK_TYPE_USAGE = 2
    paginate_by = 50

    def create_message(self, keyword, task_type, url):
        # Tweet V3
        if task_type == self.TASK_TYPE_DETAILS:
            tweet = "Help the community understand \"" + keyword + "\" by " +\
                  "enriching #stackoverflow with youtube videos you know " +\
                  "of " + url + " #stackannotator"

        elif task_type == self.TASK_TYPE_TUTORIAL:
            tweet = "Help the community understand \"" + keyword + "\" with " +\
                  "youtube tutorial videos you know of " + url + " #stackannotator"

        elif task_type == self.TASK_TYPE_USAGE:
            tweet = "Help the community understand \"" + keyword + "\" with " +\
                  "youtube usage videos you know of " + url + " #stackannotator"

        # should never happen
        else:
            tweet = "Task Error. Task Type (" + str(task_type) + ") not defined."

        return tweet


    def post(self, request, format=None):
        required_fields = ['question_id', 'answer_id', 'annotation_url',
                           'task_type', 'keyword']
        if not all (param in request.data for param in required_fields):
            errorMsg = {'Error': "Input Error",
                        'Message': "Missing fields"}
            return Response(errorMsg, status=status.HTTP_400_BAD_REQUEST)

        taskType = int(request.data['task_type'])

        if not 0 <= taskType <= 2:
            errorMsg = {'Error': "Input Error",
                        'Message': "Task Type not in range (0-2)"}
            return Response(errorMsg, status=status.HTTP_400_BAD_REQUEST)


        # create a new annotation with data
        newAnnotation = Annotation()
        newAnnotation.question_id = request.data['question_id']
        newAnnotation.answer_id = request.data['answer_id']
        newAnnotation.keyword = request.data['keyword']
        newAnnotation.save()

        appended_url = request.data['annotation_url'] + "/" \
                      + str(newAnnotation.id)
        message = self.create_message(str(request.data['keyword'][:6]+".."),
                                      taskType,
                                      appended_url)

        auth = OAuth1(settings.TWITTER_CONSUMER_KEY,
                      settings.TWITTER_CONSUMER_SECRET,
                      settings.TWITTER_ACCESS_TOKEN,
                      settings.TWITTER_ACCESS_TOKEN_SECRET)
        twitter_response = requests.post(settings.POST_STATUS_TWITTER_URL,
                                         data={'status': message}, auth=auth)
        tweet_info = twitter_response.json()
        if 'id' not in tweet_info:
            errorMsg = {'Error': "Twitter Error",
                        'Twitter Response': tweet_info.pop('errors')}
            # remove annotation we just created
            newAnnotation.delete()
            return Response(errorMsg, status=status.HTTP_400_BAD_REQUEST)

        # create a new task
        task = Task()
        task.tweet_id = tweet_info['id']
        task.annotation_id = newAnnotation.id
        task.task_type = taskType
        task.created_on = task.checked_on = timezone.now()
        task.save()

        return Response(TaskSerializer(task).data,
                        status=status.HTTP_201_CREATED)


    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

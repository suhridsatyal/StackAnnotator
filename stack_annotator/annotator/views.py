from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from annotator.models import Annotation, Video
from annotator.serializers import AnnotationSerializer, VideoSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import APIException
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

    def post(self, request, format=None):

        serializer = AnnotationSerializer(data=request.data)

        # Remember video data if a video needs to be created
        videos = request.data.get('videos', None)
        request.data["videos"] = []

        # Create annotation
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


@api_view(['POST'])
def upvote_video(request, pk):
    try:
        video = Video.objects.get(pk=pk)
        video.upvotes = video.upvotes + 1
        video.save()
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e :
        return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def downvote_video(request, pk):
    try:
        video = Video.objects.get(pk=pk)
        video.downvotes = video.downvotes + 1
        video.save()
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e :
        return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def flag_video(request, pk):
    try:
        video = Video.objects.get(pk=pk)
        video.flags = video.flags + 1
        video.save()
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e :
        return Response({"message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


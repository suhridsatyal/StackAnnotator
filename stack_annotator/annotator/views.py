from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from annotator.models import Annotation
from annotator.serializers import AnnotationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import APIException
import re

DEFAULT_LENGTH = 4

# Create your views here.
def index(request):
    return render(request, 'index.html')

class AnnotationListView(generics.ListCreateAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer

    def get_queryset(self, **kwargs):
        queryset = Annotation.objects.all()

        # Check what we received
        question_id = self.request.query_params.get('question_id', None)
        answer_id = self.request.query_params.get('answer_id', None)
        
        if question_id is not None:
            try:
                question_id = int(question_id)
            except ValueError:
                raise Http404
            queryset = queryset.filter(question_id=question_id)
            if queryset.count() < 1:
                raise Http404
        if answer_id is not None:
            try:
                answer_id = int(answer_id)
            except ValueError:
                raise Http404
            queryset = queryset.filter(answer_id=answer_id)
            if queryset.count() < 1:
                raise Http404
        return queryset

class AnnotationView(generics.RetrieveAPIView, generics.CreateAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer

    def get(self, request, **kwargs):
        queryset = Annotation.objects.all()

        #Check what we received
        annotation_id = request.query_params.get('annotation_id', None)
        question_id = self.request.query_params.get('question_id', None)
        answer_id = self.request.query_params.get('answer_id', None)

        #Support annotation/4/
        full_url_split = str(self.request.get_full_path()).split("/")
        #print(self.request.get_full_path().split("/"), len(full_url_split))

        if len(full_url_split) > DEFAULT_LENGTH:
            try:
                annotation_id = full_url_split[DEFAULT_LENGTH]
            except ValueError:
                raise Http404
            queryset = queryset.filter(id=annotation_id)
            if queryset.count() < 1:
                raise Http404
        if question_id is not None:
            try:
                question_id = int(question_id)
            except ValueError:
                raise Http404
            queryset = queryset.filter(question_id=question_id)
            if queryset.count() < 1:
                raise Http404
        if answer_id is not None:
            try:
                answer_id = int(answer_id)
            except ValueError:
                raise Http404
            queryset = queryset.filter(answer_id=answer_id)
            if queryset.count() < 1:
                raise Http404
        
        annotation = queryset.first()
        return Response(AnnotationSerializer(annotation).data, status=status.HTTP_200_OK)
 
    def post(self, request, format=None):
        serializer = AnnotationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

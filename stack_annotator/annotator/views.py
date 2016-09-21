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


def index(request):
    return render(request, 'index.html')


class AnnotationListView(generics.ListCreateAPIView):
    model = Annotation
    serializer_class = AnnotationSerializer

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

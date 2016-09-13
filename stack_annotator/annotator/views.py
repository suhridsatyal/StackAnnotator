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

# Create your views here.
def index(request):
    return render(request, 'index.html')

class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class AnnotationListByQuestion(generics.ListCreateAPIView):

    model = Annotation
    #queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

    def get_queryset(self):
        #print("Got request param", self.kwargs)
        queryset = Annotation.objects.all()
        questionID = self.request.query_params.get('questionID', self.kwargs['questionID'])
        #print("Got question param", questionID)
        if questionID is not None:
            queryset = queryset.filter(questionID=questionID)
            if queryset.count() < 1:
                raise Http404
        return queryset

class AnnotationListByAnswer(generics.ListCreateAPIView):

    model = Annotation
    serializer_class = AnnotationSerializer

    def get_queryset(self):
        queryset = Annotation.objects.all()
        answerID = self.request.query_params.get('answerID', self.kwargs['answerID'])

        if answerID is not None:
            queryset = queryset.filter(answerID=answerID)
            if queryset.count() < 1:
                raise Http404
        return queryset

#Currently using primary key to find annotation urls
class AnnotationQuery(generics.RetrieveAPIView):
    
    model = Annotation
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

    #def get_queryset(self):
        #print("Got request param", self.kwargs)
        #queryset = Annotation.objects.all()
        #annotation = self.request.query_params.get('id', self.kwargs['pk'])

        #if annotation is not None:
        #queryset = queryset.filter(id=pk)
        #if queryset.count() < 1:
        #    raise Http404
        #return queryset

class AnnotationNew(generics.CreateAPIView):
    def post(self, request, format=None):
        serializer = AnnotationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
@csrf_exempt
def annotation_list(request, stackID):
    
    List all annotations
    
    if request.method == 'GET':
        annotations = Annotation.objects.filter(stackID=stackID)
        if annotations.count() < 1:
            return HttpResponse(status=404)
        serializer = AnnotationSerializer(annotations, many=True)
        return JSONResponse(serializer.data)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def annotation_new(request):
    
	Post an annotation
	
	
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = AnnotationSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)
	else:
		return HttpResponse(status=405)
"""

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from annotator.models import Annotation
from annotator.serializers import AnnotationSerializer
from django.db import IntegrityError
import re

# Create your views here.
def index(request):
	return render(request, 'index.html')

class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def annotation_list(request, stackID):
	"""
	List all annotations
	"""
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
	"""
	Post an annotation
	"""
	
	if request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = AnnotationSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)
	else:
		return HttpResponse(status=405)

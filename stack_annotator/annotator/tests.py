from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
# from myproject.apps.core.models import Account
from .models import Annotation

def create_annotation(stackID, annotation, location):
	return Annotation.objects.create(stackID=stackID, annotation=annotation, location=location)


# Create your tests here.
class AnnotationTests(TestCase):

	def test_get_annotation(self):
		"""
		Call get on a single annotation
		"""
		client = APIClient()
		create_annotation(1, "test", 10)
		response = client.get('/annotator/1/', format='json')
		#print(response)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.content, '[{"stackID":1,"annotation":"test","location":10}]')

	def test_post_annotation(self):
		"""
		Call post to creat an annotation
		"""
		#factory = APIRequestFactory()
		client = APIClient()
		data = {"stackID":5,"annotation":"asd","location":15}
		response = client.post('/annotator/', data, format='json')
		
		#response = self.client.post('/annotator/', data, format='json')
		#print(response)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.content, '{"stackID":5,"annotation":"asd","location":15}')

	def test_get_multiple_annotation(self):
		"""
		Call get on an annotation that has multiple results
		"""
		create_annotation(1, "test", 10)
		create_annotation(4, "try", 11)
		create_annotation(1, "bad", 12)
		response = self.client.get('/annotator/1/')
		#print(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.content, '[{"stackID":1,"annotation":"test","location":10},{"stackID":1,"annotation":"bad","location":12}]')

	def test_get_fail_annotation(self):
		"""
		Call get with a id that doesn't exist
		"""
		client = APIClient()
		create_annotation(1, "test", 10)
		#response = client.get('/annotator/steroids/', format='json')
		#print(response.status_code)
		#self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		response = client.get('/annotator/90000/', format='json')
		#print(response.status_code)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_post_fail_annotation(self):
		"""
		Call post with invalid parameters
		"""
		#factory = APIRequestFactory()
		client = APIClient()
		data = {"stackID":"pie","annotation":"asd","location":15}
		response = client.post('/annotator/', data, format='json')
		
		#response = self.client.post('/annotator/', data, format='json')
		#print(response.status_code)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		#self.assertEqual(response.content, '{"stackID":5,"annotation":"asd","location":15}')
		

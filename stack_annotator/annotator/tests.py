from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
# from myproject.apps.core.models import Account
from .models import Annotation

def create_annotation(questionID, answerID, annotation, position):
    return Annotation.objects.create(questionID=questionID, answerID=answerID, annotation=annotation, position=position)


# Create your tests here.
class AnnotationTests(TestCase):

    def test_get_annotation_by_question(self):
        """
        Call get on a single annotation by question
        """
        client = APIClient()
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", 3)
        response = client.get('/annotator/question/1/', format='json')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[{"questionID":1,"answerID":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","position":7}]')

    def test_get_annotation_by_answer(self):
        """
        Call get on a single annotation by answer
        """
        client = APIClient()
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", 3)
        response = client.get('/annotator/answer/1/', format='json')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[{"questionID":2,"answerID":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","position":3}]')

    #Error here, not sure how to fix...
    def test_get_annotation_by_url(self):
        """
        Call get on a single annotation by url
        """
        client = APIClient()
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", 3)
        #url = "https://www.youtube.com/watch?v=g7zO1MBu8SQ"
        response = client.get('/annotator/annotation/2/', format='json')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '{"questionID":2,"answerID":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","position":3}')
        
    def test_post_annotation(self):
        """
        Call post to create an annotation
        """
        client = APIClient()
        data = {"questionID":5, "answerID":10, "annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","position":15}
        response = client.post('/annotator/new/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.content, '{"questionID":5,"answerID":10,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","position":15}')

    def test_get_multiple_annotation_by_question(self):
        """
        Call get on an annotation that has multiple results
        """
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", 3)
        create_annotation(1, 2, "https://www.youtube.com/watch?v=3BxYqjzMz-U", 12)
        response = self.client.get('/annotator/question/1/')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[{"questionID":1,"answerID":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","position":7},{"questionID":1,"answerID":2,"annotation":"https://www.youtube.com/watch?v=3BxYqjzMz-U","position":12}]')

    def test_get_multiple_annotation_by_answer(self):
        """
        Call get on an annotation that has multiple results
        """
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", 3)
        create_annotation(1, 2, "https://www.youtube.com/watch?v=3BxYqjzMz-U", 12)
        response = self.client.get('/annotator/answer/1/')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[{"questionID":1,"answerID":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","position":7},{"questionID":2,"answerID":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","position":3}]')

    def test_get_fail_annotation_question(self):
        """
        Call get with a id that doesn't exist
        """
        client = APIClient()
        create_annotation(1, 3, "https://www.youtube.com/watch?v=3BxYqjzMz-U", 10)
        response = client.get('/annotator/question/steroids/', format='json')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        #client = APIClient()
        response = client.get('/annotator/question/9000/', format='json')
        #print(response.status_code)
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_fail_annotation_url(self):
        """
        Call get with a id that doesn't exist
        """
        client = APIClient()
        create_annotation(1, 3, "https://www.youtube.com/watch?v=3BxYqjzMz-U", 10)
        response = client.get('/annotator/annotation/9000/', format='json')
        #print(response.status_code)
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_fail_annotation(self):
        """
        Call post with invalid parameters
        """
        #factory = APIRequestFactory()
        client = APIClient()
        data = {"questionID":"1","answerID":"1","annotation":"asd","position":15}
        response = client.post('/annotator/new/', data, format='json')

        #response = self.client.post('/annotator/', data, format='json')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #self.assertEqual(response.content, '{"stackID":5,"annotation":"asd","location":15}')


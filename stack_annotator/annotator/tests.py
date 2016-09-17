from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
# from myproject.apps.core.models import Account
from .models import Annotation

def create_annotation(question_id, answer_id, annotation, keyword, position):
    return Annotation.objects.create(question_id=question_id, answer_id=answer_id, annotation=annotation, keyword=keyword, position=position)


# Create your tests here.
class AnnotationTests(TestCase):

    def test_get_annotation_by_question(self):
        """
        Call get on a single annotation by question
        """
        client = APIClient()
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", "sting", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        response = client.get('/api/annotator/annotations?question_id=1', format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[{"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"sting","position":7}]')
        response = client.get('/api/annotator/annotation?question_id=1', format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '{"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"sting","position":7}')

    def test_get_annotation_by_annotation_id(self):
        """
        Call get on a single annotation by annotation_id
        """
        client = APIClient()
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", "sting", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        response = client.get('/api/annotator/annotations?annotation_id=1', format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[{"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"sting","position":7}]')
        response = client.get('/api/annotator/annotation?annotation_id=1', format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '{"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"sting","position":7}')

    def test_get_annotation_by_question_and_answer(self):
        """
        Call get on a single annotation by question and answer
        """
        client = APIClient()
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", "sting", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        create_annotation(1, 2, "https://www.youtube.com/watch?v=0MjdyurrP6c", "pie", 124)
        response = client.get('/api/annotator/annotations?question_id=1&answer_id=1', format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[{"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"sting","position":7}]')
        response = client.get('/api/annotator/annotation?question_id=1&answer_id=1', format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '{"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"sting","position":7}')

    def test_get_annotation_by_answer(self):
        """
        Call get on a single annotation by answer
        """
        client = APIClient()
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        response = client.get('/api/annotator/annotations?answer_id=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[{"question_id":2,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","keyword":"fiesty","position":3}]')
        response = client.get('/api/annotator/annotation?answer_id=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '{"question_id":2,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","keyword":"fiesty","position":3}')


    def test_get_annotation_by_url(self):
        """
        Call get on a single annotation by url
        """
        client = APIClient()
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", "fiesty", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "shy", 3)
        #url = "https://www.youtube.com/watch?v=g7zO1MBu8SQ"
        response = client.get('/api/annotator/annotation?annotation_id=2', format='json')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '{"question_id":2,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","keyword":"shy","position":3}')

    def test_post_annotation(self):
        """
        Call post to create an annotation
        """
        client = APIClient()
        data = {"question_id":5, "answer_id":10, "annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"fiesty","position":15}
        response = client.post('/api/annotator/annotation/', data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.content, '{"question_id":5,"answer_id":10,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"fiesty","position":15}')

    def test_get_multiple_annotation_by_question(self):
        """
        Call get on an annotation that has multiple results
        """
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", "fiesty", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        create_annotation(1, 2, "https://www.youtube.com/watch?v=3BxYqjzMz-U", "fiesty", 12)
        response = self.client.get('/api/annotator/annotations?question_id=1')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[{"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"fiesty","position":7},{"question_id":1,"answer_id":2,"annotation":"https://www.youtube.com/watch?v=3BxYqjzMz-U","keyword":"fiesty","position":12}]')

    def test_get_multiple_annotation_by_answer(self):
        """
        Call get on an annotation that has multiple results
        """
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", "fiesty", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        create_annotation(1, 2, "https://www.youtube.com/watch?v=3BxYqjzMz-U", "fiesty", 12)
        response = self.client.get('/api/annotator/annotations?answer_id=1')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[{"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"fiesty","position":7},{"question_id":2,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","keyword":"fiesty","position":3}]')

    def test_get_all_annotations(self):
        """
        Call get on all annotations
        """
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", "fiesty", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        create_annotation(1, 2, "https://www.youtube.com/watch?v=3BxYqjzMz-U", "fiesty", 12)
        response = self.client.get('/api/annotator/annotations')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[{"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"fiesty","position":7},{"question_id":2,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","keyword":"fiesty","position":3},{"question_id":1,"answer_id":2,"annotation":"https://www.youtube.com/watch?v=3BxYqjzMz-U","keyword":"fiesty","position":12}]')

    def test_get_fail_annotation_question(self):
        """
        Call get with a id that doesn't exist
        """
        client = APIClient()
        create_annotation(1, 3, "https://www.youtube.com/watch?v=3BxYqjzMz-U", "fiesty", 10)
        response = client.get('/api/annotator/annotations?question_id=steroids', format='json')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        #client = APIClient()
        response = client.get('/api/annotator/annotations?question_id=9000', format='json')
        #print(response.status_code)
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = client.get('/api/annotator/annotation?question_id=9000', format='json')
        #print(response.status_code)
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_fail_annotation_url(self):
        """
        Call get with a id that doesn't exist
        """
        client = APIClient()
        create_annotation(1, 3, "https://www.youtube.com/watch?v=3BxYqjzMz-U", "fiesty", 10)
        response = client.get('/api/annotator/annotation?annotation_id=9000', format='json')
        #print(response.status_code)
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_fail_annotation(self):
        """
        Call post with invalid parameters
        """
        #factory = APIRequestFactory()
        client = APIClient()
        data = {"question_id":"1","answer_id":"1","annotation":"asd","position":15}
        response = client.post('/api/annotator/annotation/', data, format='json')

        #response = self.client.post('/api/annotator/', data, format='json')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {"question_id":"1","answer_id":"pie","annotation":"https://www.where.com","position":15}
        response = client.post('/api/annotator/annotation/', data, format='json')

        #response = self.client.post('/api/annotator/', data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"question_id":"ety","answer_id":"1","annotation":"https://www.where.com","position":15}
        response = client.post('/api/annotator/annotation/', data, format='json')

        #response = self.client.post('/api/annotator/', data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #self.assertEqual(response.content, '{"stackID":5,"annotation":"asd","location":15}')


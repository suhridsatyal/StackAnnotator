from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from models import Annotation


def create_annotation(question_id, answer_id, annotation, keyword, position):
    return Annotation.objects.create(question_id=question_id,
            answer_id=answer_id, annotation=annotation, keyword=keyword,
            position=position)


class AnnotationAPITests(TestCase):

    def test_get_annotation_by_question(self):
        """
        Should get a single annotation by question
        """
        client = APIClient()
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c",
                "sting", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ",
                "fiesty", 3)
        response = client.get('/api/annotations?question_id=1',
                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
                '[{"id":1,"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"sting","position":7}]')


    def test_get_annotation_by_annotation_id(self):
        """
        Should get a single annotation by annotation_id 
        """
        client = APIClient()
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c",
                "sting", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ",
                "fiesty", 3)
        response = client.get('/api/annotation/2', format='json')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        response = client.get('/api/annotation/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, 
                '{"id":2,"question_id":2,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","keyword":"fiesty","position":3}')


    def test_get_annotation_by_question_and_answer(self):
        """
        Should get a single annotation by question and answer
        """
        client = APIClient()
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", "sting", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        create_annotation(1, 2, "https://www.youtube.com/watch?v=0MjdyurrP6c", "pie", 124)
        response = client.get('/api/annotations?question_id=1&answer_id=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
                '[{"id":1,"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"sting","position":7}]')


    def test_get_annotation_by_answer(self):
        """
        Should get a single annotation by answer
        """
        client = APIClient()
        create_annotation(2, 23, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "treaty", 24)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        response = client.get('/api/annotations?answer_id=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
                '[{"id":2,"question_id":2,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","keyword":"fiesty","position":3}]')


    def test_get_multiple_annotation_by_question(self):
        """
        Should filter annotation by question id
        """
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", "fiesty", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        create_annotation(1, 2, "https://www.youtube.com/watch?v=3BxYqjzMz-U", "fiesty", 12)
        response = self.client.get('/api/annotations?question_id=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
                '[{"id":1,"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"fiesty","position":7},{"id":3,"question_id":1,"answer_id":2,"annotation":"https://www.youtube.com/watch?v=3BxYqjzMz-U","keyword":"fiesty","position":12}]')


    def test_get_multiple_annotation_by_answer(self):
        """
        Should filter annotation by answer_id
        """
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", "fiesty", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        create_annotation(1, 2, "https://www.youtube.com/watch?v=3BxYqjzMz-U", "fiesty", 12)
        response = self.client.get('/api/annotations?answer_id=1')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
                '[{"id":1,"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"fiesty","position":7},{"id":2,"question_id":2,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","keyword":"fiesty","position":3}]')


    def test_get_all_annotations(self):
        """
        Should get all annotations
        """
        create_annotation(1, 1, "https://www.youtube.com/watch?v=0MjdyurrP6c", "fiesty", 7)
        create_annotation(2, 1, "https://www.youtube.com/watch?v=g7zO1MBu8SQ", "fiesty", 3)
        create_annotation(1, 2, "https://www.youtube.com/watch?v=3BxYqjzMz-U", "fiesty", 12)
        response = self.client.get('/api/annotations')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
                '[{"id":1,"question_id":1,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"fiesty","position":7},{"id":2,"question_id":2,"answer_id":1,"annotation":"https://www.youtube.com/watch?v=g7zO1MBu8SQ","keyword":"fiesty","position":3},{"id":3,"question_id":1,"answer_id":2,"annotation":"https://www.youtube.com/watch?v=3BxYqjzMz-U","keyword":"fiesty","position":12}]')


    def test_get_fail_annotation_question(self):
        """
        Should return 404 or empty response
        """
        client = APIClient()
        create_annotation(1, 3, "https://www.youtube.com/watch?v=3BxYqjzMz-U", "fiesty", 10)
        response = client.get('/api/annotations?question_id=steroids', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = client.get('/api/annotations?question_id=9000', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[]')


    def test_get_fail_annotation_url(self):
        """
        Should return 404 
        """
        client = APIClient()
        create_annotation(1, 3, "https://www.youtube.com/watch?v=3BxYqjzMz-U", "fiesty", 10)
        response = client.get('/api/annotation/9000/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_post_annotation(self):
        """
        Should create an annotation
        """
        client = APIClient()
        data = {"question_id":5, "answer_id":10, "annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"fiesty","position":15}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.content,
                '{"id":1,"question_id":5,"answer_id":10,"annotation":"https://www.youtube.com/watch?v=0MjdyurrP6c","keyword":"fiesty","position":15}')


    def test_post_fail_annotation(self):
        """
        Should fail to POST if URL is invalid
        """
        client = APIClient()

        data = {"question_id":"1","answer_id":"1","annotation":"asd","position":15}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"question_id":"1","answer_id":"pie","annotation":"https://www.where.com","position":15}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"question_id":"ety","answer_id":"1","annotation":"https://www.where.com","position":15}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


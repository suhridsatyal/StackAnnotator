from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from models import Annotation, Video


def create_annotation(question_id, answer_id, keyword, position):
    return Annotation.objects.create(question_id=question_id,
                                     answer_id=answer_id,
                                     keyword=keyword, position=position)


def create_video(video_id, annotation_id):
    return Video.objects.create(video_id=video_id,
                                annotation_id=annotation_id)


def create_video_with_details(video_id, annotation_id, upvotes, downvotes, flags, start_time):
    return Video.objects.create(video_id=video_id,
                                annotation_id=annotation_id,
                                upvotes=upvotes, downvotes=downvotes,
                                flags=flags, start_time=start_time)


class AnnotationAPITests(TestCase):


    def test_get_annotation_by_question(self):
        """
        Should get a single annotation by question
        """
        client = APIClient()
        first = create_annotation(1, 1, "sting", 7)
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty", 3)
        create_video("g7zO1MBu8SQ", second)

        response = client.get('/api/annotations?question_id=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.content)
        self.assertEqual(response.content,
            '[{"id":1,"question_id":1,"answer_id":1,"videos":[{"id":1,"video_id":"0MjdyurrP6c"}],"keyword":"sting","position":7}]')


    def test_get_annotation_by_annotation_id(self):
        """
        Should get a single annotation by annotation_id 
        """
        client = APIClient()
        first = create_annotation(1, 1, "sting", 7)
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty", 3)
        create_video("g7zO1MBu8SQ", second)
        response = client.get('/api/annotation/2', format='json')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        response = client.get('/api/annotation/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, 
                '{"id":2,"question_id":2,"answer_id":1,"videos":[{"id":2,"video_id":"g7zO1MBu8SQ"}],"keyword":"fiesty","position":3}')


    def test_get_annotation_by_question_and_answer(self):
        """
        Should get a single annotation by question and answer
        """
        client = APIClient()
        first = create_annotation(1, 1, "sting", 7)
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty", 3)
        create_video("g7zO1MBu8SQ", second)
        third = create_annotation(1, 2, "pie", 124)
        create_video("0MjdyurrP6c", third)
        response = client.get('/api/annotations?question_id=1&answer_id=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
            '[{"id":1,"question_id":1,"answer_id":1,"videos":[{"id":1,"video_id":"0MjdyurrP6c"}],"keyword":"sting","position":7}]')


    def test_get_annotation_by_answer(self):
        """
        Should get a single annotation by answer
        """
        client = APIClient()
        first = create_annotation(2, 23, "treaty", 24)
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty", 3)
        create_video("g7zO1MBu8SQ", second)
        response = client.get('/api/annotations?answer_id=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
                '[{"id":2,"question_id":2,"answer_id":1,"videos":[{"id":2,"video_id":"g7zO1MBu8SQ"}],"keyword":"fiesty","position":3}]')


    def test_get_multiple_annotation_by_question(self):
        """
        Should filter annotation by question id
        """
        first = create_annotation(1, 1, "fiesty", 7)
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty", 3)
        create_video("g7zO1MBu8SQ", second)
        third = create_annotation(1, 2, "fiesty", 12)
        create_video("3BxYqjzMz", third)
        response = self.client.get('/api/annotations?question_id=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
            '[{"id":1,"question_id":1,"answer_id":1,"videos":[{"id":1,"video_id":"0MjdyurrP6c"}],"keyword":"fiesty","position":7},{"id":3,"question_id":1,"answer_id":2,"videos":[{"id":3,"video_id":"3BxYqjzMz"}],"keyword":"fiesty","position":12}]')


    def test_get_multiple_annotation_by_answer(self):
        """
        Should filter annotation by answer_id
        """
        first = create_annotation(1, 1, "fiesty", 7)
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty", 3)
        create_video("g7zO1MBu8SQ", second)
        third = create_annotation(1, 2, "pie", 12)
        create_video("3BxYqjzMz", third)
        response = self.client.get('/api/annotations?answer_id=1')
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
                '[{"id":1,"question_id":1,"answer_id":1,"videos":[{"id":1,"video_id":"0MjdyurrP6c"}],"keyword":"fiesty","position":7},{"id":2,"question_id":2,"answer_id":1,"videos":[{"id":2,"video_id":"g7zO1MBu8SQ"}],"keyword":"fiesty","position":3}]')


    def test_get_all_annotations(self):
        """
        Should get all annotations
        """
        first = create_annotation(1, 1, "fiesty", 7)
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty", 3)
        create_video("g7zO1MBu8SQ", second)
        third = create_annotation(1, 2, "fiesty", 12)
        create_video("3BxYqjzMz", third)
        response = self.client.get('/api/annotations')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
                '[{"id":1,"question_id":1,"answer_id":1,"videos":[{"id":1,"video_id":"0MjdyurrP6c"}],"keyword":"fiesty","position":7},{"id":2,"question_id":2,"answer_id":1,"videos":[{"id":2,"video_id":"g7zO1MBu8SQ"}],"keyword":"fiesty","position":3},{"id":3,"question_id":1,"answer_id":2,"videos":[{"id":3,"video_id":"3BxYqjzMz"}],"keyword":"fiesty","position":12}]')


    def test_get_fail_annotation_question(self):
        """
        Should return 404 or empty response
        """
        client = APIClient()
        first = create_annotation(1, 3, "fiesty", 10)
        create_video("0MjdyurrP6c", first)
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
        first = create_annotation(1, 3, "fiesty", 10)
        create_video("0MjdyurrP6c", first)
        response = client.get('/api/annotation/9000/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_post_annotation(self):
        """
        Should create an annotation
        """
        client = APIClient()
        data = {"question_id":5, "answer_id":10,"videos":[],"keyword":"fiesty","position":15}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.content,
                '{"id":1,"question_id":5,"answer_id":10,"videos":[],"keyword":"fiesty","position":15}')


    def test_post_fail_annotation(self):
        """
        Should fail to POST if URL is invalid
        """
        client = APIClient()

        data = {"question_id":"1","answer_id":"pie","position":15}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"question_id":"ety","answer_id":"1","position":15}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VideoAPITests(TestCase):

    
    def test_get_all_videos(self):
        """
        Should get all videos
        """
        #video_id, annotation_id, upvotes, downvotes, flags, start_time
        first = create_annotation(1, 3, "fiesty", 10)
        create_video_with_details("0MjdyurrP6c", first, 4, 2, 0, "1:14")
        second = create_annotation(2, 1, "fiesty", 3)
        create_video_with_details("g7zO1MBu8SQ", second, 2, 1, 0, "0:14")
        third = create_annotation(1, 2, "fiesty", 12)
        create_video_with_details("3BxYqjzMz", third, 2, 1, 0, "0:14")

        client = APIClient()
        response = client.get('/api/videos', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
            '[{"id":1,"video_id":"0MjdyurrP6c","annotation_id":1,"downvotes":2,"upvotes":4,"flags":0,"start_time":"1:14"},{"id":2,"video_id":"g7zO1MBu8SQ","annotation_id":2,"downvotes":1,"upvotes":2,"flags":0,"start_time":"0:14"},{"id":3,"video_id":"3BxYqjzMz","annotation_id":3,"downvotes":1,"upvotes":2,"flags":0,"start_time":"0:14"}]')

    
    def test_get_all_videos_of_annotation(self):
        """
        Should get all videos for a particular annotation id
        """
        first = create_annotation(1, 2, "fiesty", 12)
        create_video_with_details("3BxYqjzMz", first, 4, 2, 0, "1:14")
        second = create_annotation(2, 1, "fiesty", 3)
        create_video_with_details("g7zO1MBu8SQ", second, 2, 1, 0, "0:14")
        create_video_with_details("dragonballz", second, 12, 2, 0, "0:19")

        client = APIClient()
        response = client.get('/api/videos?annotation_id=2', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
            '[{"id":2,"video_id":"g7zO1MBu8SQ","annotation_id":2,"downvotes":1,"upvotes":2,"flags":0,"start_time":"0:14"},{"id":3,"video_id":"dragonballz","annotation_id":2,"downvotes":2,"upvotes":12,"flags":0,"start_time":"0:19"}]')


    def test_get_details_of_single_video(self):
        """
        Should get a single video on a video id
        """
        first = create_annotation(1, 2, "fiesty", 12)
        create_video_with_details("3BxYqjzMz", first, 4, 2, 0, "1:14")
        create_video_with_details("dragonballz", first, 1, 9, 2, "6:17")
        create_video_with_details("demonsblade", first, 23, 2, 0, "12:14")

        client = APIClient()
        response = client.get('/api/video/2', format='json')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

        response = client.get('/api/video/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
            '{"id":2,"video_id":"dragonballz","annotation_id":1,"downvotes":9,"upvotes":1,"flags":2,"start_time":"6:17"}')

    
    def test_post_video(self):
        """
        Should post a video
        """
        create_annotation(1, 2, "fiesty", 12)

        client = APIClient()
        data = {"video_id":5, "annotation_id":1}
        response = client.post('/api/videos', data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.content,
            '{"id":1,"video_id":"5","annotation_id":1,"downvotes":0,"upvotes":0,"flags":0,"start_time":"0:00"}')


    def test_update_video(self):
        """
        Should update a video
        """
        first = create_annotation(1, 2, "fiesty", 12)
        create_video_with_details("3BxYqjzMz", first, 4, 2, 0, "1:14")

        client = APIClient()
        data = {"video_id":"updatevideo", "start_time":"13:12", "annotation_id":1}

        response = client.put('/api/video/1/', data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
            '{"id":1,"video_id":"updatevideo","annotation_id":1,"downvotes":2,"upvotes":4,"flags":0,"start_time":"13:12"}')

        response = client.get('/api/video/1/', data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
            '{"id":1,"video_id":"updatevideo","annotation_id":1,"downvotes":2,"upvotes":4,"flags":0,"start_time":"13:12"}')

        response = client.get('/api/annotation/1/', data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content,
            '{"id":1,"question_id":1,"answer_id":2,"videos":[{"id":1,"video_id":"updatevideo"}],"keyword":"fiesty","position":12}')


    def test_fail_get(self):
        """
        Should fail a get on videos
        """
        first = create_annotation(1, 2, "fiesty", 12)
        create_video_with_details("3BxYqjzMz", first, 4, 2, 0, "1:14")
        second = create_annotation(2, 1, "fiesty", 3)
        create_video_with_details("g7zO1MBu8SQ", second, 2, 1, 0, "0:14")
        create_video_with_details("dragonballz", second, 12, 2, 0, "0:19")

        client = APIClient()
        response = client.get('/api/videos?annotation_id=7', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[]')

        response = client.get('/api/videos?annotation_id=triangles', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_fail_post(self):
        """
        Should fail a post
        """
        create_annotation(1, 2, "fiesty", 12)
        #video_id, annotation_id, upvotes, downvotes, flags, start_time

        client = APIClient()
        data = {"video_id":5, "annotation_id":2}
        response = client.post('/api/videos', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"video_id":5, "annotation_id":1, "upvotes":"pie"}
        response = client.post('/api/videos', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_fail_update(self):
        """
        Should fail an update on a video
        """
        first = create_annotation(1, 2, "fiesty", 12)
        create_video_with_details("3BxYqjzMz", first, 4, 2, 0, "1:14")

        client = APIClient()
        data = {"video_id":"updatevideo", "start_time":"13:12", "annotation_id":1}

        response = client.put('/api/video/5/', data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        data = {"video_id":"updatevideo", "start_time":"13:12"}
        response = client.put('/api/video/1/', data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {"video_id":"updatevideo", "upvotes":"treetag", "annotation_id":1}
        response = client.put('/api/video/1/', data, format='json')
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

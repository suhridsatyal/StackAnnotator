from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from models import Annotation, Video
import json


def create_annotation(question_id, answer_id, keyword):
    return Annotation.objects.create(question_id=question_id,
                                     answer_id=answer_id,
                                     keyword=keyword)


def create_video(external_id, annotation_id):
    return Video.objects.create(external_id=external_id,
                                annotation_id=annotation_id)


def create_video_with_details(external_id, annotation_id, upvotes, downvotes, flags, start_time):
    return Video.objects.create(external_id=external_id,
                                annotation_id=annotation_id,
                                upvotes=upvotes, downvotes=downvotes,
                                flags=flags, start_time=start_time)


class AnnotationAPITests(TestCase):

    def test_get_annotation_by_question(self):
        """
        Should get a single annotation by question
        """
        client = APIClient()
        first = create_annotation(1, 1, "sting")
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty")
        create_video("g7zO1MBu8SQ", second)
        response = client.get('/api/annotations?question_id=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Convert json to dict
        response_dict = json.loads(response.content)[0]

        #Check if both primary keys are the same (should be enough)
        self.assertEqual(response_dict['id'], first.pk)


    def test_get_annotation_by_annotation_id(self):
        """
        Should get a single annotation by annotation_id
        """
        client = APIClient()
        first = create_annotation(1, 1, "sting")
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty")
        create_video("g7zO1MBu8SQ", second)
        
        second_pk=str(second.pk)

        response = client.get('/api/annotation/'+second_pk, format='json')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        response = client.get('/api/annotation/'+second_pk+'/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Convert json to dict
        response_dict = json.loads(response.content)

        self.assertEqual(response_dict['id'], int(second_pk))


    def test_get_annotation_by_question_and_answer(self):
        """
        Should get a single annotation by question and answer
        """
        client = APIClient()
        first = create_annotation(1, 1, "sting")
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty")
        create_video("g7zO1MBu8SQ", second)
        third = create_annotation(1, 2, "pie")
        create_video("0MjdyurrP6c", third)

        response = client.get('/api/annotations?question_id=1&answer_id=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Convert json to dict
        response_dict = json.loads(response.content)[0]

        self.assertEqual(response_dict['id'], first.pk)


    def test_get_annotation_by_answer(self):
        """
        Should get a single annotation by answer
        """
        client = APIClient()
        first = create_annotation(2, 23, "treaty")
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty")
        create_video("g7zO1MBu8SQ", second)
        response = client.get('/api/annotations?answer_id=1', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Convert json to dict
        response_dict = json.loads(response.content)[0]

        self.assertEqual(response_dict['id'], second.pk)


    def test_get_multiple_annotation_by_question(self):
        """
        Should filter annotation by question id
        """
        first = create_annotation(1, 1, "fiesty")
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty")
        create_video("g7zO1MBu8SQ", second)
        third = create_annotation(1, 2, "fiesty")
        create_video("3BxYqjzMz", third)
        response = self.client.get('/api/annotations?question_id=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Convert json to list
        response_list = json.loads(response.content)

        #Check list size is 2
        self.assertEqual(len(response_list), 2)

        for items in response_list:
            if not items['id']==first.pk and not items['id']==third.pk:
                assert False


    def test_get_multiple_annotation_by_answer(self):
        """
        Should filter annotation by answer_id
        """
        first = create_annotation(1, 1, "fiesty")
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty")
        create_video("g7zO1MBu8SQ", second)
        third = create_annotation(1, 2, "pie")
        create_video("3BxYqjzMz", third)
        response = self.client.get('/api/annotations?answer_id=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Convert json to list
        response_list = json.loads(response.content)

        #Check list size is 2
        self.assertEqual(len(response_list), 2)

        for items in response_list:
            if not items['id']==first.pk and not items['id']==second.pk:
                assert False


    def test_get_all_annotations(self):
        """
        Should get all annotations
        """
        first = create_annotation(1, 1, "fiesty")
        create_video("0MjdyurrP6c", first)
        second = create_annotation(2, 1, "fiesty")
        create_video("g7zO1MBu8SQ", second)
        third = create_annotation(1, 2, "fiesty")
        create_video("3BxYqjzMz", third)
        response = self.client.get('/api/annotations')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Convert json to list
        response_list = json.loads(response.content)

        #Check list size is 2
        self.assertEqual(len(response_list), 3)

        for items in response_list:
            if not items['id']==first.pk and not items['id']==second.pk and not items['id']==third.pk:
                assert False


    def test_get_fail_annotation_question(self):
        """
        Should return 404 or empty response
        """
        client = APIClient()
        first = create_annotation(1, 3, "fiesty")
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
        first = create_annotation(1, 3, "fiesty")
        create_video("0MjdyurrP6c", first)
        response = client.get('/api/annotation/9000/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_post_annotation(self):
        """
        Should create an annotation
        """
        client = APIClient()
        data = {"question_id":5, "answer_id":10,"videos":[],"keyword":"fiesty"}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Convert json to dict
        response_dict = json.loads(response.content)

        #Get id from post
        first_id = response_dict['id']

        data = {"question_id":5, "answer_id":10,"keyword":"fiesty","position":15}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        #Convert json to dict
        response_dict = json.loads(response.content)

        #Get id from post
        second_id = response_dict['id']

        """
        Should create an annotation with a video
        """
        data = {"question_id":5, "answer_id":10,"videos":[{"external_id":"newvideo"}],"keyword":"fiesty"}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Convert json to dict
        response_dict = json.loads(response.content)

        #Get id from post
        third_id = str(response_dict['id'])

        response = client.get('/api/annotation/'+third_id+'/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Convert json to dict
        response_dict = json.loads(response.content)

        #Check pk of annotation is the same
        self.assertEqual(response_dict['id'], int(third_id))

        #Check pk of video is the same
        self.assertEqual(response_dict['videos'][0]['external_id'], "newvideo")

        data = {"question_id":5, "answer_id":10,"videos":[{"external_id":"anothervideo","start_time":"0:15"}],"keyword":"fiesty"}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Convert json to dict
        response_dict = json.loads(response.content)

        #Get id from post
        fourth_id = str(response_dict['id'])

        response = client.get('/api/annotation/'+fourth_id+'/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Convert json to dict
        response_dict = json.loads(response.content)

        #Check pk of annotation is the same
        self.assertEqual(response_dict['id'], int(fourth_id))

        #Check pk of video is the same
        self.assertEqual(response_dict['videos'][0]['start_time'], "0:15")

    
    def test_post_fail_annotation(self):
        """
        Should fail to POST if URL is invalid
        """
        client = APIClient()

        data = {"question_id":"1","answer_id":"pie"}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"question_id":"ety","answer_id":"1"}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VideoAPITests(TestCase):

    def test_get_all_videos(self):
        """
        Should get all videos
        """
        first = create_annotation(1, 3, "fiesty")
        first_vid = create_video_with_details("0MjdyurrP6c", first, 4, 2, 0, "1:14")
        second = create_annotation(2, 1, "fiesty")
        second_vid = create_video_with_details("g7zO1MBu8SQ", second, 2, 1, 0, "0:14")
        third = create_annotation(1, 2, "fiesty")
        third_vid = create_video_with_details("3BxYqjzMz", third, 2, 1, 0, "0:14")

        client = APIClient()
        response = client.get('/api/videos', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Convert json to list
        response_list = json.loads(response.content)

        #Check list size is 2
        self.assertEqual(len(response_list), 3)

        for items in response_list:
            if not items['id']==first_vid.pk and not items['id']==second_vid.pk and not items['id']==third_vid.pk:
                assert False


    def test_get_all_videos_of_annotation(self):
        """
        Should get all videos for a particular annotation id
        """
        first = create_annotation(1, 2, "fiesty")
        first_vid = create_video_with_details("3BxYqjzMz", first, 4, 2, 0, "1:14")
        second = create_annotation(2, 1, "fiesty")
        second_vid = create_video_with_details("g7zO1MBu8SQ", second, 2, 1, 0, "0:14")
        third_vid = create_video_with_details("dragonballz", second, 12, 2, 0, "0:19")

        client = APIClient()
        response = client.get('/api/videos?annotation_id='+str(second.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Convert json to list
        response_list = json.loads(response.content)

        #Check list size is 2
        self.assertEqual(len(response_list), 2)

        for items in response_list:
            if not items['id']==second_vid.pk and not items['id']==third_vid.pk:
                assert False
        
    def test_get_details_of_single_video(self):
        """
        Should get a single video on a video id
        """
        first = create_annotation(1, 2, "fiesty")
        first_vid = create_video_with_details("3BxYqjzMz", first, 4, 2, 0, "1:14")
        second_vid = create_video_with_details("dragonballz", first, 1, 9, 2, "6:17")
        third_vid = create_video_with_details("demonsblade", first, 23, 2, 0, "12:14")

        client = APIClient()
        response = client.get('/api/video/'+str(second_vid.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

        response = client.get('/api/video/'+str(second_vid.pk)+'/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Convert json to list
        response_list = json.loads(response.content)

        self.assertEqual(response_list['id'], second_vid.pk)
        

    def test_post_video(self):
        """
        Should post a video
        """
        first = create_annotation(1, 2, "fiesty")

        client = APIClient()
        data = {"external_id":"test", "annotation_id":first.pk}
        response = client.post('/api/videos', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Convert json to list
        response_list = json.loads(response.content)

        self.assertEqual(response_list['annotation_id'], first.pk)
        self.assertEqual(response_list['external_id'], "test")
        
        """
        Post the same video
        """
        data = {"external_id":"test", "annotation_id":first.pk}
        response = client.post('/api/videos', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get('/api/videos?annotation_id='+str(first.pk), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Convert json to list
        response_list = json.loads(response.content)
        #print(response.content)
        self.assertEqual(len(response_list), 1)

    def test_update_video(self):
        """
        Should update a video
        """
        first = create_annotation(1, 2, "fiesty")
        first_vid = create_video_with_details("3BxYqjzMz", first, 4, 2, 0, "1:14")

        client = APIClient()
        data = {"external_id":"updatevideo", "start_time":"13:12", "annotation_id":first.pk}

        response = client.put('/api/video/'+str(first_vid.pk)+'/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Convert json to list
        response_list = json.loads(response.content)

        self.assertEqual(response_list['annotation_id'], first.pk)
        self.assertEqual(response_list['external_id'], "updatevideo")
        self.assertEqual(response_list['start_time'], "13:12")

        response = client.get('/api/video/'+str(first_vid.pk)+'/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Convert json to list
        response_list = json.loads(response.content)

        self.assertEqual(response_list['annotation_id'], first.pk)
        self.assertEqual(response_list['external_id'], "updatevideo")
        self.assertEqual(response_list['start_time'], "13:12")

        response = client.get('/api/annotation/'+str(first.pk)+'/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Convert json to list
        response_list = json.loads(response.content)

        self.assertEqual(response_list['id'], first.pk)
        self.assertEqual(response_list['videos'][0]['external_id'], "updatevideo")
        self.assertEqual(response_list['videos'][0]['start_time'], "13:12")


    def test_fail_get(self):
        """
        Should fail a get on videos
        """
        first = create_annotation(1, 2, "fiesty")
        create_video_with_details("3BxYqjzMz", first, 4, 2, 0, "1:14")
        second = create_annotation(2, 1, "fiesty")
        create_video_with_details("g7zO1MBu8SQ", second, 2, 1, 0, "0:14")
        create_video_with_details("dragonballz", second, 12, 2, 0, "0:19")

        client = APIClient()
        response = client.get('/api/videos?annotation_id=222', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, '[]')

        response = client.get('/api/videos?annotation_id=triangles', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
       

    def test_fail_post(self):
        """
        Should fail a post
        """
        create_annotation(1, 2, "fiesty")

        client = APIClient()
        data = {"external_id":5, "annotation_id":2}
        response = client.post('/api/videos', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"external_id":5, "annotation_id":1, "upvotes":"pie"}
        response = client.post('/api/videos', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_fail_update(self):
        """
        Should fail an update on a video
        """
        first = create_annotation(1, 2, "fiesty")
        first_vid = create_video_with_details("3BxYqjzMz", first, 4, 2, 0, "1:14")

        client = APIClient()
        data = {"external_id":"updatevideo", "start_time":"13:12", "annotation_id":first.pk}

        response = client.put('/api/video/234/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = {"external_id":"updatevideo", "start_time":"13:12"}
        response = client.put('/api/video/'+str(first_vid)+'/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = {"external_id":"updatevideo", "upvotes":"treetag", "annotation_id":first.pk}
        response = client.put('/api/video/'+str(first_vid)+'/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = {"external_id":"updatevideo", "upvotes":"2", "annotation_id":233}
        response = client.put('/api/video/'+str(first_vid)+'/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_video_upvote(self):
        """
        Should increase video upvotes
        """
        self._test_video_metadata_increment(metadata_type="upvote")
        
    def test_video_downvote(self):
        """
        Should increase video downvotes
        """
        self._test_video_metadata_increment(metadata_type="downvote")
        
    def test_video_flag(self):
        """
        Should increase video flags
        """
        self._test_video_metadata_increment(metadata_type="flag")

    def _test_video_metadata_increment(self, metadata_type):
        """
        Should upvote a video 
        """
        first = create_annotation(1, 2, "fiesty")
        client = APIClient()
        data = {"external_id":5, "annotation_id":first.pk}
        response = client.post('/api/videos', data, format='json')
        
        #Convert json to dict
        response_list = json.loads(response.content)

        vid_id = response_list['id']

        expected_attrs = ["id","external_id","annotation_id","downvotes",
                         "upvotes","flags","start_time"]

        response = client.post('/api/video/'+str(vid_id)+'/' + metadata_type, format='json')
        response_dict = json.loads(response.content)
        if not all(attrs in response_dict for attrs in expected_attrs):
            assert False
        self.assertEquals(response_dict[metadata_type+'s'], 1)
        response = client.post('/api/video/'+str(vid_id)+'/' + metadata_type, format='json')
        response_dict = json.loads(response.content)
        self.assertEquals(response_dict[metadata_type+'s'], 2)

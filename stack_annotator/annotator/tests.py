from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from models import Annotation, Video, Task

# from unittest.mock import Mock, patch
from annotator.views import TaskView
from mock import call, patch, Mock
import json


def create_annotation(question_id, answer_id, phrase):
    return Annotation.objects.create(question_id=question_id,
                                     answer_id=answer_id,
                                     phrase=phrase)


def create_video(external_id, annotation_id):
    return Video.objects.create(external_id=external_id,
                                annotation_id=annotation_id)


def create_video_with_details(external_id, annotation_id, upvotes, downvotes, flags, start_time):
    return Video.objects.create(external_id=external_id,
                                annotation_id=annotation_id,
                                upvotes=upvotes, downvotes=downvotes,
                                flags=flags, start_time=start_time)


def create_task(tweet_id, annotation, task_type, created_on, checked_on):
    return Task.objects.create(tweet_id=tweet_id,
                               task_type=task_type,
                               annotation=annotation,
                               created_on=created_on,
                               checked_on=checked_on)

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
        data = {"question_id":5, "answer_id":10, "videos":"[]", "phrase":"fiesty"}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Convert json to dict
        response_dict = json.loads(response.content)

        #Get id from post
        first_id = response_dict['id']

        data = {"question_id":5, "answer_id":10,"phrase":"fiesty","position":15}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Convert json to dict
        response_dict = json.loads(response.content)

        #Get id from post
        second_id = response_dict['id']

        """
        Should create an annotation with a video
        """
        data = {"question_id":5, "answer_id":10,"videos":"[{\"external_id\":\"newvideo\"}]","phrase":"fiesty"}
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

        data = {"question_id":5, "answer_id":10,"videos":"[{\"external_id\":\"anothervideo\",\"start_time\":\"0:15\"}]","phrase":"fiesty"}
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

        data = {"question_id":"1","answer_id":"pie", 'videos':[]}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"question_id":"ety","answer_id":"1", 'videos':[]}
        response = client.post('/api/annotations', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def _test_annotation_metadata_increment(self):
        """
        Should update understand_count of an annotation
        """
        first = create_annotation(1, 2, "fiesty")
        client = APIClient()

        #Convert json to dict
        response_list = json.loads(response.content)

        annotation_id = first.pk

        response = client.post('/api/annotation/'+str(annotation_id)+'/understand_count', format='json')
        response_dict = json.loads(response.content)
        self.assertEquals(response_dict[understand_count], 1)

        response = client.post('/api/annotation/'+str(annotation_id)+'/understand_count', format='json')
        response_dict = json.loads(response.content)
        self.assertEquals(response_dict[understand_count], 2)

        response = client.post('/api/annotation/'+str(annotation_id)+'/understand_count', format='json')
        response_dict = json.loads(response.content)
        self.assertEquals(response_dict[understand_count], 3)

        response = client.post('/api/annotation/'+str(annotation_id)+'/understand_count', format='json')
        response_dict = json.loads(response.content)
        self.assertEquals(response_dict[understand_count], 4)

        #See if report works
        response = client.get('/api/annotations/')
        #response_dict = json.loads(response.content)
        print(response.content)
        self.assertEquals(response.content, "[]")



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

    def test_filter_bad_video(self):
        """
        Should test if the filtering for a bad video
        """
        first = create_annotation(1, 2, "fiesty")
        first_vid = create_video_with_details("3BxYqjzMz", first, 4, 2, 0, "1:14")
        vid_id = first_vid.pk
        client = APIClient()
        response = client.get('/api/videos')

        #print(response.content)
        #Convert json to list
        response_list = json.loads(response.content)

        self.assertEqual(response_list[0]['annotation_id'], first.pk)
        self.assertEqual(response_list[0]['external_id'], "3BxYqjzMz")
        self.assertEqual(response_list[0]['start_time'], "1:14")

        response = client.post('/api/video/'+str(vid_id)+'/flag', format='json')
        response_dict = json.loads(response.content)
        self.assertEquals(response_dict['flags'], 1)
        response = client.post('/api/video/'+str(vid_id)+'/flag', format='json')
        response_dict = json.loads(response.content)
        self.assertEquals(response_dict['flags'], 2)
        response = client.post('/api/video/'+str(vid_id)+'/flag', format='json')
        response_dict = json.loads(response.content)
        self.assertEquals(response_dict['flags'], 3)
        response = client.post('/api/video/'+str(vid_id)+'/flag', format='json')
        response_dict = json.loads(response.content)
        self.assertEquals(response_dict['flags'], 4)

        response = client.get('/api/videos')
        self.assertEquals(response.content, "[]")


class TaskAPITests(TestCase):
    firstTask = ""
    secondTask = ""
    thirdTask = ""
    firstAnnotation = ""
    secondAnnotation = ""
    thirdAnnotation = ""

    def setUp(self):
        self.firstAnnotation = create_annotation(1, 1, "hope")
        self.firstTask = create_task("1", self.firstAnnotation, 0, "2016-12-12 12:12:12", "2016-12-12 12:12:12")
        self.secondAnnotation = create_annotation(1, 1, "hope")
        self.secondTask = create_task("2", self.secondAnnotation, 0, "2016-12-12 12:12:12", "2016-12-12 12:12:12")
        self.thirdAnnotation = create_annotation(1, 1, "hope")
        self.thirdTask = create_task("3", self.thirdAnnotation, 0, "2016-12-12 12:12:12", "2016-12-12 12:12:12")


    def test_get_task_by_id(self):
        """ Should get task by id """
        url = '/api/task/' + str(self.firstTask.pk) +'/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #expected_output = '{"id":%s,"tweet_id":"1","task_type":0,"annotation":1,"created_on":"2016-12-12T12:12:12Z","checked_on":"2016-12-12T12:12:12Z"}' % str(self.firstTask.id)

        #Convert json to list
        response_list = json.loads(response.content)

        self.assertEqual(response_list['id'], self.firstTask.pk)


    def test_get_all_tasks(self):
        """ Should get all tasks """
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Convert json to list
        response_list = json.loads(response.content)

        #Check list size is 3
        self.assertEqual(len(response_list), 3)

        for items in response_list:
            if not items['id']==self.firstTask.pk and not items['id']==self.secondTask.pk and not items['id']==self.thirdTask.pk:
                assert False

    def test_get_fail_task(self):
        """ Should fail because bad ids are provided """
        client = APIClient()

        response = client.get('/api/task/poop', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = client.get('/api/task/ss', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = client.get('/api/task/1', format='json')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)


    @patch('annotator.views.timezone.now')
    @patch('annotator.views.requests.post')
    def test_post_task(self, mock_post, mock_time):
        """ Should be successful """
        mock_post.side_effect = iter([MockGoogleShortenURLReturnSuccess(), MockTweetReturnSuccess()])
        mock_time.return_value = "2012-08-29 17:12:58"

        client = APIClient()
        data = {"question_id": 5, "answer_id": 10, "task_type": 0, "annotation_url": "fake.com", "phrase": "fiesty"}

        response = client.post('/api/tasks', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Convert json to list
        response_list = json.loads(response.content)

        new_item_id = response_list['id']

        response = client.get('/api/task/'+str(new_item_id)+'/', data)

        #Convert json to list
        response_list = json.loads(response.content)
        #print(response_list)
        self.assertEqual(response_list['task_type'], 0)
        self.assertEqual(response_list['created_on'], "2012-08-29T17:12:58Z")

        #self.assertEqual(response.content,
               #'{"id":4,"tweet_id":"1","task_type":0,"annotation":4,"created_on":"2012-08-29 17:12:58","checked_on":"2012-08-29 17:12:58"}' )


    def test_post_task_fail(self):
        """ Should fail because of missing parameter """

        client = APIClient()
        data = {"question_id": 5, "task_type": 0, "answer_id": 10, "phrase": "fiesty"}

        response = client.post('/api/tasks', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, '{"Message":"Missing fields","Error":"Input Error"}')


    @patch('annotator.views.requests.post')
    def test_post_task_tweet_fail(self, mock_post):
        """ Should fail because twitter API returns error due to duplicate tweet """
        mock_post.side_effect = iter([MockGoogleShortenURLReturnSuccess(), MockTweetReturnFail()])

        client = APIClient()
        data = {"question_id": 5, "answer_id": 10, "task_type": 0, "annotation_url": "fake.com", "phrase": "fiesty"}

        response = client.post('/api/tasks', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, '{"Twitter Response":[{"message":"Status is a duplicate.","code":187}],"Error":"Twitter Error"}')
        # AssertionError: '{"Message":"Missing fields","Error":"Input Error"}' != '{"Twitter Response":[{"message":"Status is a duplicate.","code":187}],"Error":"Twitter Error"}'


    @patch('annotator.views.requests.post')
    def test_post_task_shorten_url_fail(self, mock_post):
        """ Should fail because Google Shorten URL API returns error due to missing parameter, a problem on the backend"""
        mock_post.side_effect = iter([MockGoogleShortenURLReturnFail(), MockTweetReturnSuccess()])

        client = APIClient()
        data = {"question_id": 5, "answer_id": 10, "task_type": 0, "annotation_url": "fake.com", "phrase": "fiesty"}

        response = client.post('/api/tasks', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, '{"Google Response":{"code":400,"message":"Required","errors":[{"locationType":"parameter","domain":"global","message":"Required","reason":"required","location":"resource.longUrl"}]},"Error":"Google URL Shortener Error"}')


class MockTweetReturnSuccess:
    """ Imitates return from a tweet attempt """
    def json(self):
        # Mock tweet id
        data = {
            'id': 1,
            'created_at': "Wed Aug 29 17:12:58 +0000 2012"
        }
        return data


class MockTweetReturnFail:
    """ Imitates return from a tweet attempt """
    def json(self):
        # Mock tweet fail
        data = {
            'errors': [{'message': "Status is a duplicate.", 'code': 187}]
        }
        return data


class MockGoogleShortenURLReturnSuccess:
    """ Imitates return from a tweet attempt """
    def json(self):
        # Mock tweet fail
        data = {
            "id": "https://t.co/cgTZTvDRVS"
        }
        return data


class MockGoogleShortenURLReturnFail:
    """ Imitates return from a tweet attempt """
    def json(self):
        # Mock tweet fail
        data = {
            "error": {
                "errors": [{
                    "domain": "global",
                    "reason": "required",
                    "message": "Required",
                    "locationType": "parameter",
                    "location": "resource.longUrl"}],
                "code": 400,
                "message": "Required"
            }
        }
        return data

from rest_framework import serializers
from annotator.models import Annotation, Video, Task
from django.core.exceptions import ValidationError
import re


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'external_id', 'annotation_id', 'downvotes', 'upvotes',
                  'flags', 'start_time', 'description')


class EmbeddedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'external_id', 'downvotes', 'upvotes',
                  'flags', 'start_time', 'description')


class AnnotationSerializer(serializers.ModelSerializer):
    videos = EmbeddedVideoSerializer(source='video_set', many=True)

    class Meta:
        model = Annotation
        fields = ('id', 'question_id', 'answer_id', 'videos', 'phrase', 'understand_count')


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'tweet_id', 'task_type', 'annotation', 'created_on', 'checked_on')

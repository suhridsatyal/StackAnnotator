from rest_framework import serializers
from annotator.models import Annotation, Video
from django.core.exceptions import ValidationError
import re


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'video_id', 'annotation_id', 'downvotes', 'upvotes',
                  'flags', 'start_time')


class EmbeddedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'video_id', 'downvotes', 'upvotes',
                  'flags', 'start_time')


class AnnotationSerializer(serializers.ModelSerializer):
    videos = EmbeddedVideoSerializer(source='video_set', many=True)

    class Meta:
        model = Annotation
        fields = ('id', 'question_id', 'answer_id', 'videos', 'keyword')

from rest_framework import serializers
from annotator.models import Annotation, Video
from django.core.exceptions import ValidationError
import re


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'video_id', 'annotation_id', 'downvotes', 'upvotes',
                  'flags', 'start_time')


class ShortenedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'video_id')


class AnnotationSerializer(serializers.ModelSerializer):
    videos = ShortenedVideoSerializer(source='video_set', many=True)

    class Meta:
        model = Annotation
        fields = ('id', 'question_id', 'answer_id', 'videos', 'keyword',
                  'position')

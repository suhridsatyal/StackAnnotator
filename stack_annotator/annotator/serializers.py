from rest_framework import serializers
from annotator.models import Annotation
from django.core.exceptions import ValidationError
import re

class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ('id', 'question_id', 'answer_id', 'annotation', 'keyword', 'position')

    def validate(self, data):
        """
        Check that the URL is valid
        """
        regex = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
        if not re.match(regex, data['annotation']):
            raise serializers.ValidationError("Youtube URL is not valid.")
        return data


from rest_framework import serializers
from annotator.models import Annotation
from django.core.exceptions import ValidationError
import re

class AnnotationSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Check that the URL is valid
        """
        print(data)
        if not 'annotation' in data:
            return data
        if not re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', data['annotation']):
            raise serializers.ValidationError("URL must be a valid youtube url")
        return data    
	
    class Meta:
        model = Annotation
        fields = ('question_id', 'answer_id', 'annotation', 'position')

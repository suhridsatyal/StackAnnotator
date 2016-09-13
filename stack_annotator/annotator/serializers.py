from rest_framework import serializers
from annotator.models import Annotation
from django.core.exceptions import ValidationError
import re

class AnnotationSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Check that the URL is valid
        """
        if not re.match(r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$', data['annotation']):
            raise serializers.ValidationError("URL is not valid")
        return data    
	
    class Meta:
        model = Annotation
        fields = ('questionID', 'answerID', 'annotation', 'position')

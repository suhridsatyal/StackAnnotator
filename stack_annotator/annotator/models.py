from django.db import models

# Create your models here.
class Annotation(models.Model):
    question_id = models.IntegerField()
    answer_id = models.IntegerField()
    annotation = models.URLField()
    position = models.IntegerField()


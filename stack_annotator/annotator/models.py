from django.db import models

# Create your models here.
class Annotation(models.Model):
    questionID = models.IntegerField()
    answerID = models.IntegerField()
    annotation = models.URLField()
    position = models.IntegerField()


from django.db import models

# Create your models here.
class Annotation(models.Model):
	stackID = models.IntegerField()
	annotation = models.CharField(max_length=200)
	location = models.IntegerField()


from django.db import models
from django.contrib.postgres.fields import ArrayField


class Annotation(models.Model):
    question_id = models.IntegerField(blank=False)
    answer_id = models.IntegerField(blank=False)
    keyword = models.CharField(max_length=20, blank=False)
    position = models.IntegerField(blank=False)


class Video(models.Model):
    video_id = models.CharField(max_length=20)
    annotation_id = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    downvotes = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    flags = models.IntegerField(default=0)
    start_time = models.CharField(max_length=16, default="0:00")


class Task(models.Model):
    tweet_id = models.CharField(max_length=32, blank=False)
    annotation = models.OneToOneField(Annotation, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    checked_on = models.DateTimeField(auto_now_add=True)


class TaskCreate(models.Model):
    question_id = models.IntegerField(blank=False)
    answer_id = models.IntegerField(blank=False)
    keyword = models.CharField(max_length=20, blank=False)
    position = models.IntegerField(blank=False)

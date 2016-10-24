from django.db import models
from django.contrib.postgres.fields import ArrayField


class Annotation(models.Model):
    question_id = models.IntegerField(blank=False)
    answer_id = models.IntegerField(blank=False)
    keyword = models.CharField(max_length=20, blank=False)
    understand_count = models.IntegerField(default=0)

    def __unicode__(self):
        return "<Annotation: %s>" % self.pk


class Video(models.Model):
    external_id = models.CharField(max_length=20)
    annotation_id = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    downvotes = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    flags = models.IntegerField(default=0)
    start_time = models.CharField(max_length=16, blank=True)
    description = models.CharField(max_length=20, blank=False, default='Explanation')

    def __unicode__(self):
        return "(%s, %s) %s" % (self.pk, self.external_id,
                                self.annotation_id)


class Task(models.Model):
    tweet_id = models.CharField(max_length=32, blank=False)
    annotation = models.OneToOneField(Annotation, blank=False)
    created_on = models.DateTimeField()
    checked_on = models.DateTimeField()
    task_type = models.IntegerField(default=0)

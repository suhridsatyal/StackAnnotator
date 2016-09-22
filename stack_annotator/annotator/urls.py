from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from annotator import views

urlpatterns = [
    url(r'annotations$', views.AnnotationListView.as_view()), 
    url(r'annotation/(?P<pk>[0-9]+)/$', views.AnnotationView.as_view()),
]

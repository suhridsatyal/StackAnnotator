from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from annotator import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    #url(r'^$', views.annotation_list),
    #url(r'^(?P<pdk>[0-9]+)/$', views.annotation_detail),
    url(r'question/(?P<questionID>[0-9]+)/$', views.AnnotationListByQuestion.as_view()),
	url(r'answer/(?P<answerID>[0-9]+)/$', views.AnnotationListByAnswer.as_view()),
	url(r'annotation/(?P<pk>[0-9]+)/$', views.AnnotationQuery.as_view()),
    url(r'new/$', views.AnnotationNew.as_view()),
]

#urlpatterns = format_suffix_patterns(urlpatterns)

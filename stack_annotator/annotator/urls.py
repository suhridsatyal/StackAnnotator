from django.conf.urls import url

from annotator import views

urlpatterns = [
	#url(r'^$', views.index, name='index'),
	#url(r'^$', views.annotation_list),
    #url(r'^(?P<pdk>[0-9]+)/$', views.annotation_detail),
	url(r'^$', views.annotation_new),
    url(r'^(?P<stackID>[0-9]+)/$', views.annotation_list),
]

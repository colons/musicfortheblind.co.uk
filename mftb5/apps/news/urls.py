from django.conf.urls import patterns, url

from mftb5.apps.news import views


urlpatterns = patterns(
    '',
    url('^$', views.StoriesView.as_view(), name='stories'),
    url('^feed/$', views.StoriesFeed(), name='feed'),
    url('^(?P<slug>[^/]+)/$', views.StoryView.as_view(), name='story'),
)

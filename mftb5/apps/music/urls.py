from django.conf.urls import patterns, url

from mftb5.apps.music import views


urlpatterns = patterns(
    '',
    url('playlist$', views.PlaylistView.as_view(), name='playlist'),
)

from django.conf.urls import patterns, url

from mftb5.apps.music import views, json_views


urlpatterns = patterns(
    '',
    url('^playlist/$', json_views.PlaylistView.as_view(), name='playlist'),

    url('^(?P<album__slug>[^/]+)/(?P<slug>[^/]+)/$',
        views.TrackView.as_view(), name='track'),
    url('^(?P<album__slug>[^/]+)/(?P<slug>[^/]+)/json/$',
        json_views.TrackView.as_view(), name='track_json'),
    url('^(?P<slug>[^/]+)/$',
        views.AlbumView.as_view(), name='album'),
)

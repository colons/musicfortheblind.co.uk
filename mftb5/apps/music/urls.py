from django.conf.urls import patterns, url

from mftb5.apps.music import views, json_views
from mftb5.utils import redir


urlpatterns = patterns(
    '',
    url(r'^music/$', redir('music:album', slug='requests')),
    url(r'^music/(?P<slug>[^/]+)/$', views.MFTBRedirect.as_view()),
    url(r'^projects?/(?P<slug>[^/]+)/$', views.AlbumRedirect.as_view()),

    url('^playlist/$', json_views.PlaylistView.as_view(), name='playlist'),
    url('^albums/$', views.AlbumsView.as_view(), name='albums'),

    url('^(?P<album__slug>[^/]+)/(?P<slug>[^/]+)/$',
        views.TrackView.as_view(), name='track'),
    url('^(?P<slug>[^/]+)/$',
        views.AlbumView.as_view(), name='album'),
)

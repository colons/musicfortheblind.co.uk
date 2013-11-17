from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from mftb5.apps.music import views, json_views


def r(view, **kwargs):
    return RedirectView.as_view(url=reverse_lazy(view, kwargs=kwargs),
                                permanent=True)


urlpatterns = patterns(
    '',
    url(r'^music/$', r('music:album', slug='requests')),
    url(r'^music/(?P<slug>[^/]+)/$', views.MFTBRedirect.as_view()),
    url(r'^projects?/(?P<slug>[^/]+)/$', views.AlbumRedirect.as_view()),

    url('^playlist/$', json_views.PlaylistView.as_view(), name='playlist'),
    url('^albums/$', views.AlbumsView.as_view(), name='albums'),

    url('^(?P<album__slug>[^/]+)/(?P<slug>[^/]+)\.json$',
        json_views.TrackView.as_view(), name='track_json'),
    url('^(?P<album__slug>[^/]+)/(?P<slug>[^/]+)/$',
        views.TrackView.as_view(), name='track'),

    url('^(?P<slug>[^/]+)\.json$',
        json_views.AlbumView.as_view(), name='album_json'),
    url('^(?P<slug>[^/]+)/$',
        views.AlbumView.as_view(), name='album'),
)

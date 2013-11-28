from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView

from mftb5.utils import redir
from mftb5.views import IndexView, MetaView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^favicon.ico$',
        RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^meta/$', MetaView.as_view(), name='meta'),

    url(r'^contact/$', redir('meta')),
    url(r'^about/$', redir('meta')),

    url(r'^news/', include('mftb5.apps.news.urls', namespace='news')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('mftb5.apps.music.urls', namespace='music')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

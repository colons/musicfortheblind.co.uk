from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from mftb5.views import IndexView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url('^$', IndexView.as_view(), name='index'),
    url(r'^', include('mftb5.apps.music.urls', namespace='music')),
    url(r'^admin', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

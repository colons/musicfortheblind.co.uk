from django.conf.urls import patterns, include, url
from django.contrib import admin

from mftb5.views import IndexView


admin.autodiscover()

urlpatterns = patterns(
    '',
    url('^$', IndexView.as_view(), name='index'),
    url(r'^', include('mftb5.apps.music.urls', namespace='music')),
    url(r'^admin', include(admin.site.urls)),
)

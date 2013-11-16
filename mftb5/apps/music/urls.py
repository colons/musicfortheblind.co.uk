from django.conf.urls import patterns, url
from mftb5.apps.music.views import IndexView

urlpatterns = patterns(
    '',
    url('^$', IndexView.as_view(), name='index')
)

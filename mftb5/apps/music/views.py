from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.base import TemplateView, RedirectView

from mftb5.apps.music.mixins import (
    AlbumMixin, TrackMixin, AlbumsBreadcrumbMixin)
from mftb5.apps.music.models import Album, Track
from mftb5.mixins import PJAXResponseMixin, BreadcrumbMixin


class TrackView(TrackMixin, AlbumsBreadcrumbMixin, PJAXResponseMixin,
                DetailView):
    template_name = 'track.html'

    def get_breadcrumbs(self):
        return super(TrackView, self).get_breadcrumbs() + [
            (self.object.album.name, self.object.album.get_absolute_url())
        ]


class AlbumView(AlbumMixin, AlbumsBreadcrumbMixin, PJAXResponseMixin,
                DetailView):
    template_name = 'album.html'


class AlbumsView(BreadcrumbMixin, PJAXResponseMixin, TemplateView):
    template_name = 'albums.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AlbumsView, self).get_context_data(*args, **kwargs)
        mftb = Album.objects.get(slug="requests")
        context['albums'] = [mftb] + list(Album.objects.exclude(pk=mftb.pk))
        return context


class AlbumRedirect(AlbumMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.object.get_absolute_url()


class MFTBRedirect(RedirectView):
    model = Track

    def get_redirect_url(self, *args, **kwargs):
        return self.object.get_absolute_url()

    def get(self, *args, **kwargs):
        kwargs['album__slug'] = 'requests'
        self.object = get_object_or_404(self.model, **kwargs)
        return super(MFTBRedirect, self).get(*args, **kwargs)

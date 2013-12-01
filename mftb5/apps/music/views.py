from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, RedirectView

from mftb5.apps.music.mixins import (
    AlbumsBreadcrumbMixin, AlbumBreadcrumbMixin, TrackBreadcrumbMixin)
from mftb5.apps.music.models import Album, Track
from mftb5.mixins import PJAXResponseMixin, DetailMixin
from mftb5.views import DetailView


class TrackView(TrackBreadcrumbMixin, PJAXResponseMixin, DetailView):
    model = Track
    template_name = 'track.html'


class AlbumView(AlbumBreadcrumbMixin, PJAXResponseMixin, DetailView):
    model = Album
    template_name = 'album.html'


class AlbumsView(AlbumsBreadcrumbMixin, PJAXResponseMixin, TemplateView):
    template_name = 'albums.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AlbumsView, self).get_context_data(*args, **kwargs)
        mftb = Album.objects.get(slug="requests")

        context['albums'] = [mftb] + list(
            Album.objects.filter(published=True).exclude(pk=mftb.pk)
        )

        return context


class AlbumRedirect(DetailMixin, RedirectView):
    model = Album

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

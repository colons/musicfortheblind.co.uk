from django.views.generic import DetailView

from mftb5.apps.music.mixins import AlbumMixin, TrackMixin
from mftb5.mixins import PJAXResponseMixin, BreadcrumbMixin


class TrackView(TrackMixin, BreadcrumbMixin, PJAXResponseMixin, DetailView):
    template_name = 'track.html'

    def get_breadcrumbs(self):
        return super(TrackView, self).get_breadcrumbs() + [
            (self.object.album.name, self.object.album.get_absolute_url())
        ]


class AlbumView(AlbumMixin, BreadcrumbMixin, PJAXResponseMixin, DetailView):
    template_name = 'album.html'

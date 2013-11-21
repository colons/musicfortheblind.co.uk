from django.core.urlresolvers import reverse

from mftb5.apps.music.models import Album, Track
from mftb5.mixins import BreadcrumbMixin


class AlbumsBreadcrumbMixin(BreadcrumbMixin):
    def get_breadcrumbs(self):
        return super(AlbumsBreadcrumbMixin, self).get_breadcrumbs() + [
            ('Albums', reverse('music:albums'))
        ]


class AlbumBreadcrumbMixin(AlbumsBreadcrumbMixin):
    def get_breadcrumbs(self):
        if isinstance(self.object, Album):
            album = self.object
        elif isinstance(self.object, Track):
            album = self.object.album
        else:
            raise TypeError("I can't find an album :<")

        return super(AlbumBreadcrumbMixin, self).get_breadcrumbs() + [
            (album.name, album.get_absolute_url())
        ]


class TrackBreadcrumbMixin(AlbumBreadcrumbMixin):
    def get_breadcrumbs(self):
        return super(TrackBreadcrumbMixin, self).get_breadcrumbs() + [
            (self.object.name, self.object.get_absolute_url())
        ]

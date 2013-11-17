from django.core.urlresolvers import reverse

from mftb5.apps.music.models import Album, Track
from mftb5.mixins import DetailMixin, BreadcrumbMixin


class AlbumsBreadcrumbMixin(BreadcrumbMixin):
    def get_breadcrumbs(self):
        return super(AlbumsBreadcrumbMixin, self).get_breadcrumbs() + [
            ('Albums', reverse('music:albums'))
        ]


class TrackMixin(DetailMixin):
    model = Track


class AlbumMixin(DetailMixin):
    model = Album

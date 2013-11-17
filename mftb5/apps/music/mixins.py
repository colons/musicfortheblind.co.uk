from mftb5.apps.music.models import Album, Track
from mftb5.mixins import DetailMixin


class TrackMixin(DetailMixin):
    model = Track


class AlbumMixin(DetailMixin):
    model = Album

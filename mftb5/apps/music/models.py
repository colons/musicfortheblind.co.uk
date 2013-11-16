from os import path

from django.core.urlresolvers import reverse
from django.db import models

from mftb5.utils.mdfield import MarkdownTextField


class Album(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    date = models.DateField(blank=True, null=True)
    description = MarkdownTextField(blank=True)

    external = models.BooleanField(default=False)
    url = models.URLField(blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        if self.external:
            return self.url
        else:
            return reverse('music:album', kwargs={'slug': self.slug})


def _upload_to(instance, filename):
    return path.join(instance.album.slug, filename)


class Track(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    date = models.DateField(blank=True, null=True)
    description = MarkdownTextField(blank=True)
    lyrics = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    url = models.URLField(blank=True)

    album = models.ForeignKey('Album', blank=True, related_name='tracks')
    track_number = models.IntegerField(blank=True, null=True)

    mp3 = models.FileField(blank=True, upload_to=_upload_to)
    ogg = models.FileField(blank=True, upload_to=_upload_to)
    flac = models.FileField(blank=True, upload_to=_upload_to)
    karakoe_mp3 = models.FileField(blank=True, upload_to=_upload_to)
    karakoe_ogg = models.FileField(blank=True, upload_to=_upload_to)
    karakoe_flac = models.FileField(blank=True, upload_to=_upload_to)

    def __unicode__(self):
        return self.name

    def json(self):
        return {
            'mp3': self.mp3.url if self.mp3 else None,
            'ogg': self.ogg.url if self.ogg else None,
            'pk': self.pk,
            'name': self.name,
            'url': self.get_absolute_url(),
            'album': {
                'name': self.album.name,
                'url': self.album.get_absolute_url()
            },
        }

    def get_absolute_url(self):
        if self.external:
            return self.url
        else:
            return reverse('music:track',
                           kwargs={'slug': self.slug,
                                   'album__slug': self.album.slug})

    @property
    def external(self):
        return self.album.external

from os import path

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


def _upload_to(instance, filename):
    return path.join(instance.album.slug, filename)


class Track(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    date = models.DateField(blank=True, null=True)
    description = MarkdownTextField(blank=True)
    lyrics = models.TextField(blank=True)
    featured = models.BooleanField(default=False)

    album = models.ForeignKey('Album', blank=True)
    track_number = models.IntegerField(blank=True, null=True)

    mp3 = models.FileField(blank=True, upload_to=_upload_to)
    ogg = models.FileField(blank=True, upload_to=_upload_to)
    flac = models.FileField(blank=True, upload_to=_upload_to)
    karakoe_mp3 = models.FileField(blank=True, upload_to=_upload_to)
    karakoe_ogg = models.FileField(blank=True, upload_to=_upload_to)
    karakoe_flac = models.FileField(blank=True, upload_to=_upload_to)

    def __unicode__(self):
        return self.name

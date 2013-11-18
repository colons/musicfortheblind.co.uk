from os import path

import ujson
from markdown import markdown

from django.core.urlresolvers import reverse
from django.db import models

from mftb5.utils.mdfield import MarkdownTextField


class Album(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    date = models.DateField(blank=True, null=True)
    description = MarkdownTextField(blank=True)

    external = models.BooleanField(default=False)
    url = models.URLField(blank=True)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('music:album', kwargs={'slug': self.slug})

    def json_data(self):
        return [t.json_data() for t in self.tracks()]

    def json(self):
        return ujson.dumps(self.json_data())

    def tracks(self):
        if self.slug == 'requests':
            ordering = '-track_number'
        else:
            ordering = 'track_number'

        return self._tracks.order_by(ordering)


def _upload_to(instance, filename):
    return path.join(instance.album.slug, filename)


class Track(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    date = models.DateField(blank=True, null=True)
    description = MarkdownTextField(blank=True)
    lyrics = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    url = models.URLField(blank=True)

    album = models.ForeignKey('Album', blank=True, related_name='_tracks')
    track_number = models.IntegerField(blank=True, null=True)

    mp3 = models.FileField(blank=True, upload_to=_upload_to)
    ogg = models.FileField(blank=True, upload_to=_upload_to)
    flac = models.FileField(blank=True, upload_to=_upload_to)
    karaoke_mp3 = models.FileField(blank=True, upload_to=_upload_to,
                                   verbose_name='instrumental (mp3)')
    karaoke_ogg = models.FileField(blank=True, upload_to=_upload_to,
                                   verbose_name='instrumental (ogg)')
    karaoke_flac = models.FileField(blank=True, upload_to=_upload_to,
                                    verbose_name='instrumental (flac)')

    class Meta:
        ordering = ['track_number']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('music:track', kwargs={'slug': self.slug,
                                              'album__slug': self.album.slug})

    def json_data(self):
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

    def json(self):
        return ujson.dumps([self.json_data()])

    @property
    def external(self):
        return self.album.external

    def downloads(self):
        downloads = []
        for attr in ['mp3', 'flac', 'karaoke_mp3', 'karaoke_flac']:
            field = getattr(self, attr)
            if not field:
                continue

            url = field.url
            for field in self._meta.fields:
                if field.name == attr:
                    label = field.verbose_name
            downloads.append({'url': url, 'format': label})

        return downloads

    @classmethod
    def feature(cls):
        """ The Feature """

        return cls.objects.filter(featured=True).order_by('?')

    def truncated_description(self):
        return self.description.split('\n\n----\n\n', 1)[0]

    def truncated_description_html(self):
        return markdown(self.truncated_description())

from django.core.urlresolvers import reverse
from django.db import models

from mftb5.utils.mdfield import MarkdownTextField


class Story(models.Model):
    headline = models.CharField(max_length=300)
    deck = models.CharField(max_length=300, blank=True)
    content = MarkdownTextField()
    slug = models.SlugField()
    date = models.DateField(blank=True, null=True)

    album = models.ForeignKey('music.Album', blank=True, null=True)
    track = models.ForeignKey('music.Track', blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('news:story', kwargs={'slug': self.slug})

    def pertinent_object(self):
        if self.album:
            return self.album
        elif self.track:
            return self.track

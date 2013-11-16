import json
from os import path

from django.core.management.base import BaseCommand

from mftb5.apps.music.models import Album, Track


class Command(BaseCommand):
    args = '<dump_path>'

    def import_mftbtrack(self, thing):
        fields = thing['fields']

        track = Track(album=self.mftb)
        track.name = fields['title']
        track.slug = fields['slug']
        track.lyrics = fields['lyrics']
        track.track_number = thing['pk']

        track.save()

    def handle(self, dump_path, **kwargs):
        with open(path.expanduser(dump_path)) as dump_file:
            things = json.load(dump_file)

        if raw_input('yo, you sure? ') != 'yes':
            return

        Album.objects.all().delete()
        Track.objects.all().delete()

        self.mftb = Album(name='Music for the Blind', slug='requests')
        self.mftb.save()

        for thing in things:
            if thing['model'] == 'music.mftbtrack':
                self.import_mftbtrack(thing)

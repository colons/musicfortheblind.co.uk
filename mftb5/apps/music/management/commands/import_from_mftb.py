import json
from os import path

from django.core.management.base import BaseCommand

from mftb5.apps.music.models import Album, Track


class Command(BaseCommand):
    args = '<dump_path>'

    def import_project(self, thing):
        fields = thing['fields']
        album = Album(
            pk=thing['pk'],
            name=fields['name'],
            external=bool(fields['external']),
            date=fields['date'],
            description=fields['comments'],
            slug=fields['slug']
        )
        album.save()

    def import_mftbtrack(self, thing):
        fields = thing['fields']

        track = Track(
            album=self.mftb,
            name=fields['title'],
            slug=fields['slug'],
            lyrics=fields['lyrics'],
            date=fields['date'],
            track_number=thing['pk'],
        )

        featured = self.models['music.feature'][0]['fields']['mftb_tracks']
        if thing['pk'] in featured:
            track.featured = True

        track.save()

    def import_othertrack(self, thing):
        fields = thing['fields']
        track = Track(
            name=fields['title'],
            lyrics=fields['lyrics'],
            description=fields['comments'],
            slug=fields['slug'],
            track_number=fields['tracknum'],
            album=Album.objects.get(pk=fields['project'])
        )

        featured = self.models['music.feature'][0]['fields']['other_tracks']
        if thing['pk'] in featured:
            track.featured = True

        track.save()

    def handle(self, dump_path, **kwargs):
        with open(path.expanduser(dump_path)) as dump_file:
            things = json.load(dump_file)

        # if raw_input('yo, you sure? ') != 'yes':
        #     return

        Album.objects.all().delete()
        Track.objects.all().delete()

        self.mftb = Album(name='Music for the Blind', slug='requests')
        self.mftb.save()

        self.models = {
            'music.client': [],
            'music.codeproject': [],
            'music.mftbtrack': [],
            'music.mftbvolume': [],
            'music.project': [],
            'music.othertrack': [],
            'music.creator': [],
            'music.mftbcredit': [],
            'music.string': [],
            'music.newsitem': [],
            'music.feature': [],
        }

        for thing in things:
            self.models[thing['model']].append(thing)

        for thing in self.models['music.mftbtrack']:
            self.import_mftbtrack(thing)

        for thing in self.models['music.project']:
            self.import_project(thing)

        for thing in self.models['music.othertrack']:
            self.import_othertrack(thing)

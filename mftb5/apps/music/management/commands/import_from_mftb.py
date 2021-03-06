import ujson
from os import path

from django.core.files import File
from django.core.management.base import BaseCommand

from mftb5.apps.music.models import Album, Track
from mftb5.apps.news.models import Story


class Command(BaseCommand):
    args = '<dump_path> <media_dir>'

    def import_project(self, thing):
        fields = thing['fields']
        album = Album(
            pk=thing['pk'],
            name=fields['name'],
            external=fields['slug'] == 'pyrrha',
            date=fields['date'],
            description=fields['comments'],
            slug=fields['slug'],
            url=fields['url'],
        )
        album.save()

    def import_mftbtrack(self, thing):
        the_dir = path.join(self.media_dir, 'music', 'mftb')
        fields = thing['fields']

        if fields['client_credit_implicit']:
            description = fields['request']
        else:
            for client in self.models['music.client']:
                if client['pk'] == fields['client']:
                    the_client = client['fields']['name']
                    break

            fmt = '%s\n\n-%s'

            if fields['is_quote']:
                fmt = '> ' + fmt

            description = fmt % (fields['request'], the_client)

        credit_already = False

        for credit in self.models['music.mftbcredit']:
            if credit['fields']['track'] == thing['pk']:
                for creator in self.models['music.creator']:
                    if creator['pk'] == credit['fields']['creator']:
                        the_creator = creator
                        break

                if credit['fields']['url']:
                    role_string = '[%s](%s)' % (
                        credit['fields']['role'],
                        credit['fields']['url']
                    )
                else:
                    role_string = credit['fields']['role']

                if the_creator['fields']['home']:
                    creator_string = '[%s](%s)' % (
                        the_creator['fields']['name'],
                        the_creator['fields']['home']
                    )
                else:
                    creator_string = the_creator['fields']['name']

                credit_string = '%s by %s' % (role_string, creator_string)

                if credit_already:
                    breaker = '\n\n'
                else:
                    breaker = '\n\n----\n\n'

                description = description + breaker + credit_string

                credit_already = True

        if fields['comments']:
            description = (
                description + '\n\n----\n\n' +
                fields['comments'].replace('\r\n', '\n\n')
            )

        track = Track(
            album=self.mftb,
            name=fields['title'],
            slug=fields['slug'],
            lyrics=fields['lyrics'],
            date=fields['date'],
            track_number=thing['pk'],
            description=description
        )

        featured = self.models['music.feature'][0]['fields']['mftb_tracks']
        if thing['pk'] in featured:
            track.featured = True

        for field, fmt, dest in [
            ('mp3', '%04i_%s.mp3', 'mp3'),
            ('flac', '%04i_%s.flac', 'flac'),
            ('karaoke', '%04i_%s.karaoke.mp3', 'karaoke_mp3'),
        ]:
            if fields[field]:
                file_path = path.join(the_dir, fmt
                                      % (track.track_number, track.slug))
                basename = path.basename(file_path)

                with open(file_path) as the_file:
                    getattr(track, dest).save(basename, File(the_file,
                                                             name=basename))

        track.save()

    def import_othertrack(self, thing):
        fields = thing['fields']
        album = Album.objects.get(pk=fields['project'])
        track = Track(
            name=fields['title'],
            lyrics=fields['lyrics'],
            description=fields['comments'],
            slug=fields['slug'],
            track_number=fields['tracknum'],
            url=fields['page_url'],
            album=album,
            date=fields.get('date', None),
        )
        the_dir = path.join(self.media_dir, 'music', album.slug)

        for field, fmt, dest in [
            ('mp3', '%s.mp3', 'mp3'),
            ('flac', '%s.flac', 'flac'),
            ('karaoke', '%s.karaoke.mp3', 'karakoe_mp3'),
        ]:
            if fields[field]:
                if track.track_number is not None:
                    fmt = '%02i_%s' % (track.track_number, fmt)

                file_path = path.join(the_dir, fmt % track.slug)
                basename = path.basename(file_path)

                with open(file_path) as the_file:
                    getattr(track, dest).save(basename, File(the_file,
                                                             name=basename))

        featured = self.models['music.feature'][0]['fields']['other_tracks']
        if thing['pk'] in featured:
            track.featured = True

        track.save()

    def import_newsitem(self, thing):
        fields = thing['fields']

        if fields['mftb']:
            track = Track.objects.get(
                album=self.mftb,
                track_number=fields['mftb'],
            )
        else:
            track = None

        content = fields['pre_jump'] + '\n\n' + fields['post_jump']

        for source, dest in {
            '</div>': '</figure>',
            '<div class="figkey">': '<figure>',
            '<div class="fig">': '<figure class="sub">',
            '<div class="figleft">': '<figure class="sub alt">',
        }.iteritems():
            content = content.replace(source, dest)

        story = Story(
            headline=fields['headline'],
            date=fields['date'],
            content=content,
            deck=fields['summary'],
            slug=fields['slug'],
            track=track,
        )

        story.save()

    def handle(self, dump_path, media_dir, **kwargs):
        with open(path.expanduser(dump_path)) as dump_file:
            things = ujson.load(dump_file)

        # XXX
        # if raw_input('yo, you sure? ') != 'yes':
        #     return

        assert path.isdir(media_dir)
        self.media_dir = media_dir

        Album.objects.all().delete()
        Track.objects.all().delete()
        Story.objects.all().delete()

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

        for thing in self.models['music.project']:
            self.import_project(thing)

        self.mftb = Album(name='Music for the Blind', slug='requests')
        self.mftb.save()

        for thing in self.models['music.othertrack']:
            self.import_othertrack(thing)

        for album in Album.objects.all():
            tracks = album.tracks()
            track_numbers = [t.track_number for t in tracks]

            if set(track_numbers) == set([1]):
                for track in tracks:
                    track.track_number = None
                    track.save()

        for thing in self.models['music.mftbtrack']:
            self.import_mftbtrack(thing)

        for thing in self.models['music.newsitem']:
            self.import_newsitem(thing)

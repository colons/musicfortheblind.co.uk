import json

from django.http import HttpResponse
from django.views.generic import View

from mftb5.apps.music.models import Track


class JSONView(View):
    def get(self, request, *args, **kwargs):
        data = self.get_json_data(request, *args, **kwargs)
        return HttpResponse(json.dumps(data), content_type='application/json')


class PlaylistView(JSONView):
    def get_json_data(self, request):
        if 'playlist' in request.session:
            playlist = [Track.objects.get(pk=pk)
                        for pk in request.session['playlist']]
        else:
            playlist = Track.objects.filter(featured=True).order_by('?')
            request.session['playlist'] = [t.pk for t in playlist]

        return [
            # XXX gonna need to put useful urls in here
            {
                'mp3': t.mp3.url,
                'pk': t.pk,
                'name': t.name,
                'album': {
                    'name': t.album.name,
                },
            }
            for t in playlist
        ]

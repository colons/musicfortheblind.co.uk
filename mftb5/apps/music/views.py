import json

from django.http import HttpResponse
from django.views.generic import View, DetailView

from mftb5.utils.pjax import PJAXResponseMixin

from mftb5.apps.music.models import Album, Track


class TrackView(PJAXResponseMixin, DetailView):
    template_name = 'track.html'
    model = Track


class AlbumView(PJAXResponseMixin, DetailView):
    template_name = 'album.html'
    model = Album


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

        return [t.json() for t in playlist]

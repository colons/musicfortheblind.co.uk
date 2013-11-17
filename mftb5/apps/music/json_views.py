import json

from django.http import HttpResponse
from django.views.generic import View

from mftb5.apps.music.models import Track


class JSONView(View):
    def get(self, request, *args, **kwargs):
        data = self.get_json_data(request)
        return HttpResponse(json.dumps(data), content_type='application/json')


class PlaylistView(JSONView):
    """
    This whole thing is gross.
    """

    def post(self, request):
        # rudimentary validation, liable to 500
        try:
            pks = [int(pk) for pk in request.POST.getlist('id', [])]
            selected_str = request.POST.get('selected')

            if selected_str != 'undefined':
                selected = int(selected_str)
                print selected
            else:
                selected = None

            for pk in pks:
                Track.objects.get(pk=pk)  # validation!

            assert (selected is None) or (selected in pks)

            request.session['playlist'] = pks
            request.session['selected'] = selected
            return HttpResponse()
        except:
            self.reset_playlist(request)
            raise

    def get_json_data(self, request):
        if 'playlist' in request.session:
            try:
                playlist = [Track.objects.get(pk=pk)
                            for pk in request.session['playlist']]
            except:
                self.reset_playlist(request)
                raise
        else:
            playlist = self.reset_playlist(request)

        selected = request.session.get('selected')

        if selected not in (p.pk for p in playlist):
            selected = playlist[0].pk

        return {
            'playlist': [t.json_data() for t in playlist],
            'selected': selected,
        }

    def reset_playlist(self, request):
        playlist = [t.pk for t in Track.feature()]
        request.session['playlist'] = playlist
        return playlist

import json

from django.http import HttpResponse
from django.views.generic import View

from mftb5.apps.music.models import Track


class JSONView(View):
    def get(self, request, *args, **kwargs):
        data = self.get_json_data(request)
        return HttpResponse(json.dumps(data), content_type='application/json')


def coercible_to_int(string):
    try:
        int(string)
    except ValueError:
        return False
    else:
        return True


class PlaylistView(JSONView):
    """
    This whole thing is gross.
    """

    def post(self, request):
        pks = [int(pk) for pk in request.POST.getlist('id', [])
               if coercible_to_int(pk) and
               Track.objects.filter(pk=int(pk)).exists()]

        selected_str = request.POST.get('selected')

        if selected_str != 'undefined':
            selected = int(selected_str)
        else:
            selected = None

        assert (selected is None) or (selected in pks)

        request.session['playlist'] = pks
        request.session['selected'] = selected
        request.session['stranger'] = bool(int(request.POST['stranger']))
        return HttpResponse()

    def get_json_data(self, request):
        pks = request.session.get('playlist')
        selected = request.session.get('selected')

        if not pks:
            playlist = Track.feature()
            pks = [t.pk for t in playlist]
        else:
            playlist = [Track.objects.get(pk=pk) for pk in pks]

        if selected is None or selected not in pks:
            selected = playlist[0].pk

        return {
            'playlist': [t.json_data() for t in playlist],
            'selected': selected,
        }

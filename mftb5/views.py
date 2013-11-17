from django.views.generic.base import TemplateView

from mftb5.apps.music.models import Album
from mftb5.utils.pjax import PJAXResponseMixin


class IndexView(PJAXResponseMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['albums'] = Album.objects.all()
        return context

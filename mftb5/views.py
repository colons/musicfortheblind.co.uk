from django.views.generic.base import TemplateView

from mftb5.utils.pjax import PJAXResponseMixin


class IndexView(PJAXResponseMixin, TemplateView):
    template_name = 'index.html'

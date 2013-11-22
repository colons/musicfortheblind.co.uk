import ujson

from django.views.generic import DetailView as DjangoDetailView
from django.views.generic.base import TemplateView

from mftb5.apps.music.models import Album, Track
from mftb5.apps.news.models import Story
from mftb5.mixins import PJAXResponseMixin, DetailMixin, ContactBreadcrumbMixin


class IndexView(PJAXResponseMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)

        feature = list(Track.feature())

        context['albums'] = Album.objects.all()
        context['stories'] = Story.objects.all()
        context['feature'] = ujson.dumps([t.json_data() for t in feature])
        context['first_track'] = feature[0]
        context['stranger'] = self.request.session.get('stranger', True)
        print dict(self.request.session)
        return context


class ContactView(ContactBreadcrumbMixin, PJAXResponseMixin, TemplateView):
    template_name = 'contact.html'


class DetailView(DetailMixin, DjangoDetailView):
    """ A utility view for apps to use."""

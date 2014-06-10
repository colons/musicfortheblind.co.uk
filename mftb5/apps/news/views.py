from django.core.urlresolvers import reverse_lazy
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.views.generic import DetailView
from django.views.generic import ListView

from mftb5.apps.news.mixins import StoriesBreadcrumbMixin, StoryBreadcrumbMixin
from mftb5.apps.news.models import Story
from mftb5.mixins import PJAXResponseMixin


class StoryView(StoryBreadcrumbMixin, PJAXResponseMixin, DetailView):
    template_name = 'story.html'
    model = Story


class StoriesView(StoriesBreadcrumbMixin, PJAXResponseMixin, ListView):
    template_name = 'stories.html'
    queryset = Story.objects.filter(published=True)


class StoriesFeed(Feed):
    feed_type = Atom1Feed
    link = reverse_lazy('news:stories')
    title = 'Music for the Blind News'
    subtitle = 'New music and other occasional updates'

    def items(self):
        return Story.objects.all()

    def item_description(self, item):
        return item.content_html

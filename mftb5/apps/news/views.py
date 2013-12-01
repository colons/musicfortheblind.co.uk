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

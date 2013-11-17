from django.views.generic import DetailView
from django.views.generic import ListView

from mftb5.apps.news.mixins import StoriesBreadcrumbMixin
from mftb5.apps.news.models import Story
from mftb5.mixins import PJAXResponseMixin, BreadcrumbMixin


class StoryView(StoriesBreadcrumbMixin, PJAXResponseMixin, DetailView):
    template_name = 'story.html'
    model = Story


class StoriesView(BreadcrumbMixin, PJAXResponseMixin, ListView):
    template_name = 'stories.html'
    model = Story

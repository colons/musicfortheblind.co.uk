from django.core.urlresolvers import reverse

from mftb5.mixins import BreadcrumbMixin


class StoriesBreadcrumbMixin(BreadcrumbMixin):
    def get_breadcrumbs(self):
        return super(StoriesBreadcrumbMixin, self).get_breadcrumbs() + [
            ('News', reverse('news:stories'))
        ]


class StoryBreadcrumbMixin(StoriesBreadcrumbMixin):
    def get_breadcrumbs(self):
        return super(StoryBreadcrumbMixin, self).get_breadcrumbs() + [
            (self.object.headline, self.object.get_absolute_url())
        ]

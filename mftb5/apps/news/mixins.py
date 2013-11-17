from django.core.urlresolvers import reverse

from mftb5.mixins import BreadcrumbMixin


class StoriesBreadcrumbMixin(BreadcrumbMixin):
    def get_breadcrumbs(self):
        return super(StoriesBreadcrumbMixin, self).get_breadcrumbs() + [
            ('News', reverse('news:stories'))
        ]

from django.test import TestCase

from instant_coverage import InstantCoverageMixin, optional

from mftb5.apps.music.models import Track, Album
from mftb5.apps.news.models import Story


base_covered_urls = {
    '/',
    '/meta/',
    '/contact/',
    '/about/',
    '/news/',
    '/news/blade-teardown/',
    '/music/',
    '/albums/',
    '/playlist/',
    '/music/dust/',
    '/orphans/',
    '/projects/orphans/',
}


class EverythingTest(
    optional.ValidHTML5,
    optional.ValidJSON,
    InstantCoverageMixin, TestCase
):
    fixtures = ['music', 'news']
    spelling_language = 'en_GB'

    uncovered_urls = [
        '/favicon.ico',
    ]
    uncovered_includes = [
        ('^admin/',),
    ]
    instant_tracebacks = True

    def setUp(self):
        if not self.covered_urls:
            covered_urls = set(base_covered_urls)

            for model in [Track, Album, Story]:
                for instance in model.objects.all():
                    covered_urls.add(instance.get_absolute_url())

            self.covered_urls = list(covered_urls)

        self.assertGreater(len(self.covered_urls), len(base_covered_urls))

        super(EverythingTest, self).setUp()

from django.test import TestCase

from instant_coverage import InstantCoverageMixin


class EverythingTest(InstantCoverageMixin, TestCase):
    fixtures = ['music', 'news']

    covered_urls = [
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
        '/projects/thrust/',
        '/orphans/',
        '/pyrrha/pyrrha/',
    ]
    uncovered_urls = [
        '/favicon.ico',
    ]
    uncovered_includes = [
        ('^admin/',),
    ]
    instant_tracebacks = True

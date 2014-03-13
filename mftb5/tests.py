from django.test import TestCase

from instant_coverage import InstantCoverageMixin, optional


from mftb5.apps.music.models import Track, Album

covered_urls = {
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
}


for model in [Track, Album]:
    for instance in model.objects.all():
        covered_urls.add(instance.get_absolute_url())


class EverythingTest(
    optional.ValidHTML5,
    optional.ValidJSON,
    InstantCoverageMixin, TestCase
):
    fixtures = ['music', 'news']
    spelling_language = 'en_GB'

    covered_urls = list(covered_urls)
    uncovered_urls = [
        '/favicon.ico',
    ]
    uncovered_includes = [
        ('^admin/',),
    ]
    instant_tracebacks = True

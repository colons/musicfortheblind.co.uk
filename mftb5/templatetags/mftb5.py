from urlparse import urlparse

from django.template import Library

register = Library()


@register.filter
def service_from_url(url):
    host = urlparse(url).netloc

    if host.startswith('www.'):
        host = host[4:]

    bandcamp = 'Download on Bandcamp'

    return {
        'soundcloud.com': 'Listen on SoundCloud',
        'nivi.bandcamp.com': bandcamp,
        'desus.bandcamp.com': bandcamp,
        'globalgamejam.org': 'See the game on The Global Game Jam',
        'moddb.com': 'See the game on Mod DB',
        'youtube.com': 'Watch on YouTube',
    }.get(host, host)

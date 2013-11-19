from urlparse import urlparse

from django.template import Library

register = Library()


@register.filter
def service_from_url(url):
    host = urlparse(url).netloc

    if host.startswith('www.'):
        host = host[4:]

    return {
        'soundcloud.com': 'listen on SoundCloud',
        'nivi.bandcamp.com': 'download on Bandcamp',
        'globalgamejam.org': 'see the game on The Global Game Jam',
        'moddb.com': 'see the game on Mod DB',
    }.get(host, host)

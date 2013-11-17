from urlparse import urlparse

from django.template import Library

register = Library()


@register.filter
def service_from_url(url):
    host = urlparse(url).netloc
    return host

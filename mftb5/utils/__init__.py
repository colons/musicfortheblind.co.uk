from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView


def redir(view, **kwargs):
    """
    A quick way to make an internal redirect in a urlconf.
    """

    return RedirectView.as_view(url=reverse_lazy(view, kwargs=kwargs),
                                permanent=True)

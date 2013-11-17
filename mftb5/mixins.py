from django.core.urlresolvers import reverse


class BreadcrumbMixin(object):
    def get_breadcrumbs(self):
        return [('Home', reverse('index'))]

    def get_context_data(self, *args, **kwargs):
        context = super(BreadcrumbMixin, self).get_context_data(*args,
                                                                **kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


class PJAXResponseMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(PJAXResponseMixin, self
                        ).get_context_data(*args, **kwargs)

        if self.request.META.get('HTTP_X_PJAX', False):
            context['parent'] = 'pjax.html'
        else:
            context['parent'] = 'base.html'

        return context


class DetailMixin(object):
    def get(self, *args, **kwargs):
        self.object = self.model.objects.get(**kwargs)
        return super(DetailMixin, self).get(*args, **kwargs)

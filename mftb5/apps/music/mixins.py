from mftb5.apps.music.models import Track


class TrackMixin(object):
    model = Track

    def get(self, *args, **kwargs):
        self.object = self.model.objects.get(**kwargs)
        return super(TrackMixin, self).get(*args, **kwargs)

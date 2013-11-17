from django.contrib import admin
from mftb5.apps.music.models import Album, Track

for model in [Album, Track]:
    admin.site.register(model)

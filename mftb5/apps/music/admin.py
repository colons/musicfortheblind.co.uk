from django.contrib import admin
from mftb5.apps.music.models import Album, Track


class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'album', 'track_number')
    list_filter = ('album', 'published')
    ordering = ('album', 'track_number')


admin.site.register(Album)
admin.site.register(Track, TrackAdmin)

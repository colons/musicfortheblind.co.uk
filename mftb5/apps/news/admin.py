from django.contrib import admin
from mftb5.apps.news.models import Story

for model in [Story]:
    admin.site.register(model)

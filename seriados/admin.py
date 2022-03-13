from atexit import register

from django.contrib import admin

from . import models
from .models import Serie

admin.site.register(models.Serie)
admin.site.register(models.Temporada)
admin.site.register(models.Episodio)

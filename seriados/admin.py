from atexit import register

from django.contrib import admin

from . import models

admin.site.register(models.Serie)
admin.site.register(models.Temporada)
admin.site.register(models.Episodio)

# Inserindo página administrativa do blog

# admin.site.register(Postagem)

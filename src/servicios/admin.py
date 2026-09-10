from django.contrib import admin

from servicios import models

admin.site.register(models.Cliente)
admin.site.register(models.Servicio)

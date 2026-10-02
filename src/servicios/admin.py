from django.contrib import admin
from django.db.models import Sum

from servicios import models


@admin.register(models.Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono", "email", "cantidad_solicitudes")
    search_fields = ("nombre", "email", "telefono")
    ordering = ("nombre",)

    @admin.display(description="Solicitudes")
    def cantidad_solicitudes(self, obj: models.Cliente) -> int:
        return obj.solicitudes.count()


@admin.register(models.Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion_corta")
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)

    @admin.display(description="Descripción")
    def descripcion_corta(self, obj: models.Servicio) -> str:
        if not obj.descripcion:
            return "-"
        return obj.descripcion[:60] + ("…" if len(obj.descripcion) > 60 else "")


class PagoInline(admin.TabularInline):
    model = models.Pago
    extra = 1
    readonly_fields = ("fecha",)


@admin.register(models.SolicitudServicio)
class SolicitudServicioAdmin(admin.ModelAdmin):
    list_display = (
        "servicio",
        "cliente",
        "estado",
        "estado_pago",
        "monto_total",
        "total_pagado",
        "fecha",
    )
    list_filter = ("estado", "estado_pago", "servicio", "fecha")
    search_fields = ("cliente__nombre", "servicio__nombre", "descripcion")
    autocomplete_fields = ("cliente", "servicio")
    readonly_fields = ("fecha", "total_pagado")
    date_hierarchy = "fecha"
    ordering = ("-fecha",)
    inlines = (PagoInline,)

    @admin.display(description="Pagado")
    def total_pagado(self, obj: models.SolicitudServicio):
        return obj.pagos.aggregate(total=Sum("monto"))["total"] or 0


@admin.register(models.Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("solicitud", "monto", "fecha")
    list_filter = ("fecha",)
    search_fields = ("solicitud__cliente__nombre", "solicitud__servicio__nombre")
    readonly_fields = ("fecha",)
    ordering = ("-fecha",)

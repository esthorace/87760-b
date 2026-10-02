from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = "servicios"

urlpatterns = [
    path("", TemplateView.as_view(template_name="servicios/index.html"), name="index"),
    path("servicio/list", servicio_list, name="servicio_list"),
    path("servicio/create", servicio_create, name="servicio_create"),
    path("servicio/detail/<int:pk>", servicio_detail, name="servicio_detail"),
    path("servicio/update/<int:pk>", servicio_update, name="servicio_update"),
    path("servicio/delete/<int:pk>", servicio_delete, name="servicio_delete"),
    path("cliente/list", ClienteList.as_view(), name="cliente_list"),
    path("cliente/create", ClienteCreate.as_view(), name="cliente_create"),
    path("cliente/detail/<int:pk>", ClienteDetail.as_view(), name="cliente_detail"),
    path("cliente/update/<int:pk>", ClienteUpdate.as_view(), name="cliente_update"),
    path("cliente/delete/<int:pk>", ClienteDelete.as_view(), name="cliente_delete"),
    path("solicitud/list", SolicitudServicioList.as_view(), name="solicitud_list"),
    path("solicitud/create", SolicitudServicioCreate.as_view(), name="solicitud_create"),
    path("solicitud/detail/<int:pk>", SolicitudServicioDetail.as_view(), name="solicitud_detail"),
    path("solicitud/update/<int:pk>", SolicitudServicioUpdate.as_view(), name="solicitud_update"),
    path("solicitud/delete/<int:pk>", SolicitudServicioDelete.as_view(), name="solicitud_delete"),
    path("pago/list", PagoList.as_view(), name="pago_list"),
    path("pago/create", PagoCreate.as_view(), name="pago_create"),
    path("pago/detail/<int:pk>", PagoDetail.as_view(), name="pago_detail"),
    path("pago/update/<int:pk>", PagoUpdate.as_view(), name="pago_update"),
    path("pago/delete/<int:pk>", PagoDelete.as_view(), name="pago_delete"),
]

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
]

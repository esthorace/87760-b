from django.urls import path

from servicios.views import cliente_list, index, servicio_list

app_name = "servicios"

urlpatterns = [
    path("", index, name="index"),
    path("servicio/list", servicio_list, name="servicio_list"),
    path("cliente/list", cliente_list, name="cliente_list"),
]

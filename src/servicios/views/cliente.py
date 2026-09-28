__all__ = ["ClienteCreate", "ClienteDelete", "ClienteDetail", "ClienteList", "ClienteUpdate"]

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..forms import ClienteForm
from ..models import Cliente


class ClienteList(ListView):
    model = Cliente
    context_object_name = "clientes"

    def get_queryset(self):
        busqueda = self.request.GET.get("busqueda", "").strip()
        if busqueda:
            return Cliente.objects.filter(nombre__icontains=busqueda)
        return Cliente.objects.all()


class ClienteCreate(CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("servicios:cliente_list")


class ClienteDetail(DetailView):
    model = Cliente
    context_object_name = "cliente"


class ClienteUpdate(UpdateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("servicios:cliente_list")


class ClienteDelete(DeleteView):
    model = Cliente
    success_url = reverse_lazy("servicios:cliente_list")

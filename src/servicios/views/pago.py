__all__ = ["PagoCreate", "PagoDelete", "PagoDetail", "PagoList", "PagoUpdate"]

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..forms import PagoForm
from ..models import Pago


class PagoList(ListView):
    model = Pago
    context_object_name = "pagos"

    def get_queryset(self):
        return Pago.objects.select_related("solicitud")


class PagoCreate(CreateView):
    model = Pago
    form_class = PagoForm
    success_url = reverse_lazy("servicios:pago_list")


class PagoDetail(DetailView):
    model = Pago
    context_object_name = "pago"


class PagoUpdate(UpdateView):
    model = Pago
    form_class = PagoForm
    success_url = reverse_lazy("servicios:pago_list")


class PagoDelete(DeleteView):
    model = Pago
    success_url = reverse_lazy("servicios:pago_list")

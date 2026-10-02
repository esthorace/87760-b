__all__ = [
    "SolicitudServicioCreate",
    "SolicitudServicioDelete",
    "SolicitudServicioDetail",
    "SolicitudServicioList",
    "SolicitudServicioUpdate",
]

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..forms import SolicitudServicioForm
from ..models import SolicitudServicio


class SolicitudServicioList(ListView):
    model = SolicitudServicio
    context_object_name = "solicitudes"

    def get_queryset(self):
        busqueda = self.request.GET.get("busqueda", "").strip()
        if busqueda:
            return SolicitudServicio.objects.filter(
                cliente__nombre__icontains=busqueda
            ).select_related("cliente", "servicio")
        return SolicitudServicio.objects.select_related("cliente", "servicio")


class SolicitudServicioCreate(CreateView):
    model = SolicitudServicio
    form_class = SolicitudServicioForm
    success_url = reverse_lazy("servicios:solicitud_list")


class SolicitudServicioDetail(DetailView):
    model = SolicitudServicio
    context_object_name = "solicitud"


class SolicitudServicioUpdate(UpdateView):
    model = SolicitudServicio
    form_class = SolicitudServicioForm
    success_url = reverse_lazy("servicios:solicitud_list")


class SolicitudServicioDelete(DeleteView):
    model = SolicitudServicio
    success_url = reverse_lazy("servicios:solicitud_list")

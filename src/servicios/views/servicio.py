__all__ = [
    "servicio_create",
    "servicio_delete",
    "servicio_detail",
    "servicio_list",
    "servicio_update",
]

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..forms import ServicioForm
from ..models import Servicio


def servicio_list(request: HttpRequest) -> HttpResponse:
    busqueda = request.GET.get("busqueda", "").strip()
    if busqueda:
        servicios = Servicio.objects.filter(nombre__icontains=busqueda)
    else:
        servicios = Servicio.objects.all()
    return render(request, "servicios/servicio_list.html", {"servicios": servicios})


def servicio_create(request: HttpRequest) -> HttpResponse:
    match request.method:
        case "POST":
            form = ServicioForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("servicios:servicio_list")
        case _:
            form = ServicioForm()
    return render(request, "servicios/servicio_form.html", {"form": form})


def servicio_detail(request: HttpRequest, pk: int) -> HttpResponse:
    servicio = Servicio.objects.get(id=pk)
    return render(request, "servicios/servicio_detail.html", {"servicio": servicio})


def servicio_update(request: HttpRequest, pk: int) -> HttpResponse:
    servicio = Servicio.objects.get(id=pk)

    match request.method:
        case "POST":
            form = ServicioForm(request.POST, instance=servicio)
            if form.is_valid():
                form.save()
                return redirect("servicios:servicio_list")
        case _:
            form = ServicioForm(instance=servicio)

    return render(request, "servicios/servicio_form.html", {"form": form})


def servicio_delete(request: HttpRequest, pk: int) -> HttpResponse:
    servicio = Servicio.objects.get(id=pk)
    match request.method:
        case "POST":
            servicio.delete()
            return redirect("servicios:servicio_list")
        case _:
            return render(
                request,
                "servicios/servicio_confirm_delete.html",
                {"servicio": servicio},
            )

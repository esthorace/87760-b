from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from servicios.forms import ClienteForm, ServicioForm
from servicios.models import Cliente, Servicio


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "servicios/index.html")


def servicio_list(request: HttpRequest) -> HttpResponse:
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


class ClienteList(ListView):
    model = Cliente
    context_object_name = "clientes"


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

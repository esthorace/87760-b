from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from servicios.models import Cliente, Servicio


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "servicios/index.html")


def servicio_list(request: HttpRequest) -> HttpResponse:
    servicios = Servicio.objects.all()
    return render(request, "servicios/servicio_list.html", {"servicios": servicios})


def cliente_list(request: HttpRequest) -> HttpResponse:
    clientes = Cliente.objects.all()
    return render(request, "servicios/cliente_list.html", {"clientes": clientes})

from datetime import UTC, datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    mensaje = input("Dime tu mensaje: ")
    contexto = {"titulo": "Servicios", "mensaje": mensaje, "fecha": datetime.now(UTC)}
    return render(request, "core/index.html", contexto)

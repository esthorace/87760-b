from datetime import UTC, datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    contexto = {
        "titulo": "Servicios",
        "mensaje": "Aplicación Web para ofrecer servicios",
        "fecha": datetime.now(UTC),
    }
    return render(request, "core/index.html", contexto)

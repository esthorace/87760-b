from datetime import UTC, datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms import RegisterForm


def index(request: HttpRequest) -> HttpResponse:
    contexto = {
        "titulo": "Servicios",
        "mensaje": "Aplicación Web para ofrecer servicios",
        "fecha": datetime.now(UTC),
    }
    return render(request, "core/index.html", contexto)


def ejercicio2(request):
    usuarios = [
        {"nombre": "juan", "email": "juan@django"},
        {"nombre": "santi", "email": "juan@django"},
        {"nombre": "agustín", "email": "juan@django"},
    ]
    return render(request, "core/ejercicio2.html", {"usuarios": usuarios})


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "core/register.html"
    success_url = reverse_lazy("core:login")

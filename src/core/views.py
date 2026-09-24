from datetime import UTC, datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy


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


# class Login(LoginView):
#     template_name = "core/login.html"
#     # authentication_form = AuthenticationForm
#     next_page = reverse_lazy("core:index")
#     # success_message = "Inicio de sesión exitoso"

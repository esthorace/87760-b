from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from core.views import RegisterView, ejercicio2, index

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    path("ejercicio2/", ejercicio2, name="ejercicio2"),
    path("login/", LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="core/logout.html"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]

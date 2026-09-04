from django.urls import path

from core.views import ejercicio2, index

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    path("ejercicio2/", ejercicio2, name="ejercicio2"),
]

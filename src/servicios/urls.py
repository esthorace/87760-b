from django.urls import path

from servicios.views import index

app_name = "servicios"

urlpatterns = [
    path("", index, name="index"),
]

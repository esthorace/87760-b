from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from servicios.models import (
    Cliente,
    EstadoPago,
    EstadoServicio,
    Pago,
    Servicio,
    SolicitudServicio,
)


class EstadoServicioTests(TestCase):
    def test_valores_del_enum(self) -> None:
        self.assertEqual(EstadoServicio.SOLICITADO, "solicitado")
        self.assertEqual(EstadoServicio.EN_CURSO, "en curso")
        self.assertEqual(EstadoServicio.TERMINADO, "terminado")
        self.assertEqual(len(EstadoServicio.choices), 3)


class EstadoPagoTests(TestCase):
    def test_valores_del_enum(self) -> None:
        self.assertEqual(EstadoPago.IMPAGO, "impago")
        self.assertEqual(EstadoPago.PAGO_PARCIAL, "pago parcial")
        self.assertEqual(EstadoPago.PAGO_TOTAL, "pago total")
        self.assertEqual(len(EstadoPago.choices), 3)


class SolicitudServicioModelTests(TestCase):
    def setUp(self) -> None:
        self.cliente = Cliente.objects.create(nombre="Cliente de prueba")
        self.servicio = Servicio.objects.create(nombre="Servicio de prueba")

    def test_creacion_con_defaults(self) -> None:
        solicitud = SolicitudServicio.objects.create(
            cliente=self.cliente, servicio=self.servicio
        )
        self.assertEqual(solicitud.estado, EstadoServicio.SOLICITADO)
        self.assertEqual(solicitud.estado_pago, EstadoPago.IMPAGO)
        self.assertEqual(solicitud.monto_total, 0)

    def test_str(self) -> None:
        solicitud = SolicitudServicio.objects.create(
            cliente=self.cliente,
            servicio=self.servicio,
            estado=EstadoServicio.EN_CURSO,
        )
        self.assertEqual(str(solicitud), "Servicio de prueba - Cliente de prueba (En curso)")

    def test_relacion_con_pagos(self) -> None:
        solicitud = SolicitudServicio.objects.create(
            cliente=self.cliente, servicio=self.servicio, monto_total=100
        )
        Pago.objects.create(solicitud=solicitud, monto=40)
        self.assertEqual(solicitud.pagos.count(), 1)


class PagoModelTests(TestCase):
    def setUp(self) -> None:
        self.cliente = Cliente.objects.create(nombre="Cliente de prueba")
        self.servicio = Servicio.objects.create(nombre="Servicio de prueba")
        self.solicitud = SolicitudServicio.objects.create(
            cliente=self.cliente, servicio=self.servicio, monto_total=100
        )

    def test_str(self) -> None:
        pago = Pago.objects.create(solicitud=self.solicitud, monto=50)
        self.assertEqual(str(pago), f"Pago 50 - {self.solicitud}")


class BaseSesionTests(TestCase):
    """Las vistas del CRUD requieren sesión (LoginRequiredMiddleware)."""

    def setUp(self) -> None:
        self.usuario = User.objects.create_user(username="ana", password="clave-segura-123")
        self.cliente = Cliente.objects.create(nombre="Cliente de prueba")
        self.servicio = Servicio.objects.create(nombre="Servicio de prueba")
        self.solicitud = SolicitudServicio.objects.create(
            cliente=self.cliente, servicio=self.servicio, monto_total=100
        )
        self.pago = Pago.objects.create(solicitud=self.solicitud, monto=50)


class SolicitudServicioViewTests(BaseSesionTests):
    def test_list_requiere_sesion(self) -> None:
        response = self.client.get(reverse("servicios:solicitud_list"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("core:login")))

    def test_list_con_sesion(self) -> None:
        self.client.force_login(self.usuario)
        response = self.client.get(reverse("servicios:solicitud_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Servicio de prueba")

    def test_list_con_busqueda(self) -> None:
        self.client.force_login(self.usuario)
        response = self.client.get(
            reverse("servicios:solicitud_list"), {"busqueda": "Cliente de prueba"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Servicio de prueba")

    def test_create_con_sesion(self) -> None:
        self.client.force_login(self.usuario)
        url = reverse("servicios:solicitud_create")
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(
            url,
            {
                "cliente": self.cliente.pk,
                "servicio": self.servicio.pk,
                "descripcion": "Trabajo de prueba",
                "estado": EstadoServicio.SOLICITADO,
                "estado_pago": EstadoPago.IMPAGO,
                "monto_total": 250,
            },
        )
        self.assertRedirects(response, reverse("servicios:solicitud_list"))
        self.assertEqual(SolicitudServicio.objects.count(), 2)

    def test_detail_update_delete_con_sesion(self) -> None:
        self.client.force_login(self.usuario)
        detail = self.client.get(
            reverse("servicios:solicitud_detail", kwargs={"pk": self.solicitud.pk})
        )
        self.assertEqual(detail.status_code, 200)

        update = self.client.post(
            reverse("servicios:solicitud_update", kwargs={"pk": self.solicitud.pk}),
            {
                "cliente": self.cliente.pk,
                "servicio": self.servicio.pk,
                "descripcion": "Actualizada",
                "estado": EstadoServicio.TERMINADO,
                "estado_pago": EstadoPago.PAGO_TOTAL,
                "monto_total": 100,
            },
        )
        self.assertRedirects(update, reverse("servicios:solicitud_list"))
        self.solicitud.refresh_from_db()
        self.assertEqual(self.solicitud.estado, EstadoServicio.TERMINADO)
        self.assertEqual(self.solicitud.estado_pago, EstadoPago.PAGO_TOTAL)

        delete_get = self.client.get(
            reverse("servicios:solicitud_delete", kwargs={"pk": self.solicitud.pk})
        )
        self.assertEqual(delete_get.status_code, 200)
        delete = self.client.post(
            reverse("servicios:solicitud_delete", kwargs={"pk": self.solicitud.pk})
        )
        self.assertRedirects(delete, reverse("servicios:solicitud_list"))
        self.assertFalse(SolicitudServicio.objects.filter(pk=self.solicitud.pk).exists())


class PagoViewTests(BaseSesionTests):
    def test_list_requiere_sesion(self) -> None:
        response = self.client.get(reverse("servicios:pago_list"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("core:login")))

    def test_list_con_sesion(self) -> None:
        self.client.force_login(self.usuario)
        response = self.client.get(reverse("servicios:pago_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "50")

    def test_create_con_sesion(self) -> None:
        self.client.force_login(self.usuario)
        url = reverse("servicios:pago_create")
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(url, {"solicitud": self.solicitud.pk, "monto": 30})
        self.assertRedirects(response, reverse("servicios:pago_list"))
        self.assertEqual(Pago.objects.count(), 2)

    def test_detail_update_delete_con_sesion(self) -> None:
        self.client.force_login(self.usuario)
        detail = self.client.get(
            reverse("servicios:pago_detail", kwargs={"pk": self.pago.pk})
        )
        self.assertEqual(detail.status_code, 200)

        update = self.client.post(
            reverse("servicios:pago_update", kwargs={"pk": self.pago.pk}),
            {"solicitud": self.solicitud.pk, "monto": 75},
        )
        self.assertRedirects(update, reverse("servicios:pago_list"))
        self.pago.refresh_from_db()
        self.assertEqual(self.pago.monto, 75)

        delete_get = self.client.get(
            reverse("servicios:pago_delete", kwargs={"pk": self.pago.pk})
        )
        self.assertEqual(delete_get.status_code, 200)
        delete = self.client.post(
            reverse("servicios:pago_delete", kwargs={"pk": self.pago.pk})
        )
        self.assertRedirects(delete, reverse("servicios:pago_list"))
        self.assertFalse(Pago.objects.filter(pk=self.pago.pk).exists())

from urllib.parse import parse_qs, urlparse

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from servicios.models import Cliente, Servicio

# Vistas que deben ser accesibles sin iniciar sesión.
VISTAS_PUBLICAS = ["core:about", "core:index", "core:login", "core:register"]


class LoginRequiredMiddlewareTests(TestCase):
    """Comprueba que LoginRequiredMiddleware protege todas las vistas
    salvo las exentas con @login_not_required.
    """

    def setUp(self) -> None:
        self.usuario = User.objects.create_user(username="ana", password="clave-segura-123")
        self.cliente = Cliente.objects.create(nombre="Cliente de prueba")
        self.servicio = Servicio.objects.create(nombre="Servicio de prueba")

    def rutas_protegidas(self) -> list[tuple[str, dict, str]]:
        """(nombre de la vista, kwargs, ruta esperada en next)."""
        return [
            ("core:ejercicio2", {}, "/ejercicio2/"),
            ("servicios:index", {}, "/servicios/"),
            ("servicios:cliente_list", {}, "/servicios/cliente/list"),
            ("servicios:cliente_create", {}, "/servicios/cliente/create"),
            (
                "servicios:cliente_detail",
                {"pk": self.cliente.pk},
                f"/servicios/cliente/detail/{self.cliente.pk}",
            ),
            (
                "servicios:cliente_update",
                {"pk": self.cliente.pk},
                f"/servicios/cliente/update/{self.cliente.pk}",
            ),
            (
                "servicios:cliente_delete",
                {"pk": self.cliente.pk},
                f"/servicios/cliente/delete/{self.cliente.pk}",
            ),
            ("servicios:servicio_list", {}, "/servicios/servicio/list"),
            ("servicios:servicio_create", {}, "/servicios/servicio/create"),
            (
                "servicios:servicio_detail",
                {"pk": self.servicio.pk},
                f"/servicios/servicio/detail/{self.servicio.pk}",
            ),
            (
                "servicios:servicio_update",
                {"pk": self.servicio.pk},
                f"/servicios/servicio/update/{self.servicio.pk}",
            ),
            (
                "servicios:servicio_delete",
                {"pk": self.servicio.pk},
                f"/servicios/servicio/delete/{self.servicio.pk}",
            ),
        ]

    # --- Vistas públicas -------------------------------------------------

    def test_vistas_exentas_accesibles_sin_sesion(self) -> None:
        for nombre in VISTAS_PUBLICAS:
            with self.subTest(vista=nombre):
                response = self.client.get(reverse(nombre))
                self.assertEqual(response.status_code, 200)

    def test_logout_es_publico_y_no_redirige_a_login(self) -> None:
        # LogoutView solo acepta POST, así que GET responde 405 y nunca
        # redirige al login: la vista está exenta del middleware.
        response = self.client.get(reverse("core:logout"))
        self.assertEqual(response.status_code, 405)

    # --- Vistas protegidas ------------------------------------------------

    def test_vistas_protegidas_redirigen_a_login_sin_sesion(self) -> None:
        for nombre, kwargs, ruta in self.rutas_protegidas():
            with self.subTest(vista=nombre):
                response = self.client.get(reverse(nombre, kwargs=kwargs))
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, f"{reverse('core:login')}?next={ruta}")

    def test_vistas_protegidas_accesibles_con_sesion(self) -> None:
        self.client.force_login(self.usuario)
        for nombre, kwargs, _ in self.rutas_protegidas():
            with self.subTest(vista=nombre):
                response = self.client.get(reverse(nombre, kwargs=kwargs))
                self.assertEqual(response.status_code, 200)

    def test_tras_iniciar_sesion_se_vuelve_a_la_vista_original(self) -> None:
        ruta = reverse("servicios:servicio_list")
        destino = self.client.get(ruta).url
        next_url = parse_qs(urlparse(destino).query)["next"][0]
        self.assertEqual(next_url, ruta)

        self.client.force_login(self.usuario)
        self.assertEqual(self.client.get(next_url).status_code, 200)

    # --- Admin -----------------------------------------------------------

    def test_admin_login_es_publico(self) -> None:
        response = self.client.get(reverse("admin:login"))
        self.assertEqual(response.status_code, 200)

    def test_admin_redirige_a_su_propio_login(self) -> None:
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("admin:login")))

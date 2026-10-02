from django.db import models


class EstadoServicio(models.TextChoices):
    SOLICITADO = "solicitado", "Solicitado"
    EN_CURSO = "en curso", "En curso"
    TERMINADO = "terminado", "Terminado"


class EstadoPago(models.TextChoices):
    IMPAGO = "impago", "Impago"
    PAGO_PARCIAL = "pago parcial", "Pago parcial"
    PAGO_TOTAL = "pago total", "Pago total"


class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self) -> str:
        return self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class SolicitudServicio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="solicitudes")
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, related_name="solicitudes")
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=EstadoServicio.choices,
        default=EstadoServicio.SOLICITADO,
    )
    estado_pago = models.CharField(
        max_length=20,
        choices=EstadoPago.choices,
        default=EstadoPago.IMPAGO,
    )
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.servicio} - {self.cliente} ({self.get_estado_display()})"


class Pago(models.Model):
    solicitud = models.ForeignKey(SolicitudServicio, on_delete=models.CASCADE, related_name="pagos")
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Pago {self.monto} - {self.solicitud}"

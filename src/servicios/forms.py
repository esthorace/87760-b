from django import forms

from servicios.models import Cliente, Pago, Servicio, SolicitudServicio


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = "__all__"


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"


class SolicitudServicioForm(forms.ModelForm):
    class Meta:
        model = SolicitudServicio
        fields = "__all__"


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = "__all__"

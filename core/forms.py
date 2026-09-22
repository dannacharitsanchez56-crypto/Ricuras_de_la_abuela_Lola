from django import forms
from .models import InformacionRestaurante

class InformacionRestauranteForm(forms.ModelForm):
    class Meta:
        model = InformacionRestaurante
        fields = ['direccion', 'telefono', 'horario']

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import InformacionRestaurante


class InformacionRestauranteForm(forms.ModelForm):
    class Meta:
        model = InformacionRestaurante
        fields = ['direccion', 'telefono', 'horario']


class AdminCrearForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo")
    first_name = forms.CharField(label="Nombre", required=True)
    last_name = forms.CharField(label="Apellido", required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user


class AdminEditarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Nombre', 'last_name': 'Apellido', 'email': 'Correo'}
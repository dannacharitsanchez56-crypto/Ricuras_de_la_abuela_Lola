
from django import forms
from .models import Plato, Resena


class PlatoForm(forms.ModelForm):

    class Meta:
        model = Plato

        fields = [
            'nombre',
            'descripcion',
            'precio',
            'categoria',
            'imagen',
            'disponible',
        ]

        labels = {
            'nombre': 'Nombre del plato',
            'descripcion': 'Descripción',
            'precio': 'Precio (COP)',
            'categoria': 'Categoría',
            'imagen': 'Imagen del plato',
            'disponible': 'Disponible',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Bandeja paisa',
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': (
                    'Describe el plato, sus ingredientes '
                    'y preparación.'
                ),
            }),

            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Ej: 15000',
            }),

            'categoria': forms.Select(attrs={
                'class': 'form-control',
            }),

            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),

            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not nombre or not nombre.strip():
            raise forms.ValidationError(
                'El nombre del plato es obligatorio.'
            )

        return nombre.strip()

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')

        if precio is None or precio <= 0:
            raise forms.ValidationError(
                'El precio debe ser mayor que cero.'
            )

        return precio


class ResenaForm(forms.ModelForm):

    class Meta:
        model = Resena

        fields = [
            'estrellas',
            'comentario',
        ]

        labels = {
            'estrellas': 'Calificación',
            'comentario': 'Tu opinión',
        }

        widgets = {
            'estrellas': forms.Select(attrs={
                'class': 'form-control',
            }),

            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': (
                    'Cuéntanos qué te pareció este plato...'
                ),
            }),
        }

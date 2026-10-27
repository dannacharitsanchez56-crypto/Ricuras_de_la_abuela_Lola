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
            'precio': 'Precio',
            'categoria': 'Categoría',
            'imagen': 'Imagen del plato',
            'disponible': 'Disponible',
        }

        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Describe el plato, ingredientes, preparación, etc.'
            }),

            'precio': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': 'Ej: 15000'
            }),

            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
        }



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
                'class': 'form-control'
            }),

            'comentario': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Cuéntanos qué te pareció este plato...',
                'class': 'form-control'
            }),
        }
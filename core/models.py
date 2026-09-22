from django.db import models


class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True) 
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class InformacionRestaurante(models.Model):
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    horario = models.CharField(max_length=200)

    def __str__(self):
        return "Información del restaurante"
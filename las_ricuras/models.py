from django.db import models


class Plato(models.Model):
    CATEGORIAS = [
        ('entrada', 'Entrada'),
        ('plato_fuerte', 'Plato fuerte'),
        ('postre', 'Postre'),
        ('bebida', 'Bebida'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS,
        default='plato_fuerte'
    )
    imagen = models.ImageField(
        upload_to='platos/',
        blank=True,
        null=True
    )
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
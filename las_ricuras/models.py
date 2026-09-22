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

    imagen = models.ImageField(
        upload_to='platos/',
        blank=True,
        null=True
    )

    disponible = models.BooleanField(
        default=True
    )

    categoria = models.CharField(
        max_length=30,
        choices=CATEGORIAS,
        default='plato_fuerte'
    )

    def __str__(self):
        return self.nombre


class Producto(models.Model):

    nombre = models.CharField(max_length=100)

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    unidad = models.CharField(
        max_length=20
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    disponible = models.BooleanField(
        default=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nombre
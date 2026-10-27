from django.db import models
from django.conf import settings

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
        max_length=30,
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
    

class Venta(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # El total se calcula solo: precio del plato x cantidad
        self.total = self.plato.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre} - ${self.total}"



class Pedido(models.Model):
    mesero = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    mesa = models.CharField(max_length=20, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_total(self):
        self.total = sum(d.subtotal() for d in self.detalles.all())
        self.save()

    def __str__(self):
        return f"Pedido #{self.id}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="detalles", on_delete=models.CASCADE)
    plato = models.ForeignKey("Plato", on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.plato.precio * self.cantidad
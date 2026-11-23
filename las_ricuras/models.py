from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Plato(models.Model):
    CATEGORIAS = [
        ('entrada', 'Entrada'),
        ('plato_fuerte', 'Plato fuerte'),
        ('postre', 'Postre'),
        ('bebida', 'Bebida'),
        
    ]
    
    personalizable = models.BooleanField(
        default=False, 
        verbose_name="¿Permitir personalizar almuerzo?")

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
    unidad = models.CharField(max_length=20)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    disponible = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    plato = models.ForeignKey(
        Plato,
        on_delete=models.PROTECT
    )
    cantidad = models.PositiveIntegerField(default=1)
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        self.total = self.plato.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre} - ${self.total}"


# Nuevo modelo exclusivo para registrar montos de ventas manualmente
class RegistroVenta(models.Model):
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta registrada - ${self.total}"



class Resena(models.Model):
    ESTRELLAS = [
        (1, '1 Estrella'),
        (2, '2 Estrellas'),
        (3, '3 Estrellas'),
        (4, '4 Estrellas'),
        (5, '5 Estrellas'),
    ]

    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    estrellas = models.IntegerField(
        choices=ESTRELLAS,
        default=5
    )

    comentario = models.TextField()
    
    
    respuesta_admin = models.TextField(blank=True, null=True, verbose_name="Respuesta del Administrador")

    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ('plato', 'usuario')

    def __str__(self):
        return f"Reseña de {self.usuario.username} - {self.plato.nombre}"
    
class OpcionesAlmuerzo(models.Model):
    plato = models.OneToOneField(
        'Plato',
        on_delete=models.CASCADE,
        related_name='configuracion_cuadros'
    )

    proteinas = models.JSONField(
        default=list,
        blank=True
    )

    principios = models.JSONField(
        default=list,
        blank=True
    )

    acompanamientos = models.JSONField(
        default=list,
        blank=True
    )

    def __str__(self):
        return f'Opciones de {self.plato.nombre}'


class PedidoConEleccion(models.Model):

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    plato = models.ForeignKey(
        'Plato',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    nombre_plato = models.CharField(max_length=200)
    proteina = models.CharField(max_length=80)
    principio = models.CharField(max_length=80)
    acompanamiento = models.CharField(max_length=80)

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    estado = models.CharField(
        max_length=12,
        choices=ESTADOS,
        default='pendiente'
    )

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido #{self.pk} - {self.nombre_plato}'
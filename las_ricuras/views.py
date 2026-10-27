from django.contrib import messages
from .models import Plato, Pedido, DetallePedido
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from urllib.parse import quote
import io
import qrcode
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Plato
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from .models import Venta
from django.contrib.admin.views.decorators import staff_member_required

from .models import Plato
from .forms import PlatoForm
from .decorators import solo_staff


def portada(request):
    return render(request, 'portada.html')


def inicio(request):
    contexto = {
        'metodos': [
            {'nombre': 'Nequi', 'icono': '📱'},
            {'nombre': 'Efectivo', 'icono': '💵'},
            {'nombre': 'Bancolombia', 'icono': '🏦'},
        ]
    }
    return render(request, 'inicio.html', contexto)


def menu(request):
    platos = Plato.objects.all().order_by('-disponible', 'nombre')
    return render(request, 'menu.html', {'platos': platos})


# --- AQUÍ ESTÁ LA FUNCIÓN DE CONTACTO QUE FALTABA ---
def contacto(request):
    contexto = {
        'metodos': [
            {'nombre': 'Nequi', 'icono': '📱'},
            {'nombre': 'Efectivo', 'icono': '💵'},
            {'nombre': 'Bancolombia', 'icono': '🏦'},
        ]
    }
    return render(request, 'contacto.html', contexto)


@login_required
def perfil(request):
    return render(request, 'perfil.html')


@solo_staff
def Platos(request):
    platos = Plato.objects.all()
    return render(request, 'Platos.html', {'platos': platos})


def plato_detalle(request, id):
    plato = get_object_or_404(Plato, id=id)
    return render(request, 'plato_detalle.html', {'plato': plato})


@solo_staff
def crear_plato(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato creado correctamente.')
            return redirect('Platos')
    else:
        form = PlatoForm()
    return render(request, 'plato_form.html', {'form': form})


@solo_staff
def editar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES, instance=plato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato actualizado correctamente.')
            return redirect('Platos')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'plato_form.html', {'form': form, 'plato': plato})


@solo_staff
def eliminar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == 'POST':
        plato.delete()
        messages.success(request, 'Plato eliminado correctamente.')
        return redirect('Platos')
    return render(request, 'plato_confirmar_eliminar.html', {'plato': plato})


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password1 or not password2:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'registro.html')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')

        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'registro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya está en uso.')
            return render(request, 'registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ese correo electrónico ya está registrado.')
            return render(request, 'registro.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.save()
            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al crear la cuenta: {str(e)}')
            return render(request, 'registro.html')

    return render(request, 'registro.html')





@login_required
def perfil(request):
    return render(request, 'perfil.html')


@solo_staff
def Platos(request):
    platos = Plato.objects.all()
    return render(request, 'Platos.html', {'platos': platos})


def plato_detalle(request, id):
    plato = get_object_or_404(Plato, id=id)
    return render(request, 'plato_detalle.html', {'plato': plato})


@solo_staff
def crear_plato(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato creado correctamente.')
            return redirect('Platos')
    else:
        form = PlatoForm()
    return render(request, 'plato_form.html', {'form': form})


@solo_staff
def editar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES, instance=plato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plato actualizado correctamente.')
            return redirect('Platos')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'plato_form.html', {'form': form, 'plato': plato})


@solo_staff
def eliminar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == 'POST':
        plato.delete()
        messages.success(request, 'Plato eliminado correctamente.')
        return redirect('Platos')
    return render(request, 'plato_confirmar_eliminar.html', {'plato': plato})


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password1 or not password2:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'registro.html')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')

        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'registro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya está en uso.')
            return render(request, 'registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Ese correo electrónico ya está registrado.')
            return render(request, 'registro.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.save()
            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al crear la cuenta: {str(e)}')
            return render(request, 'registro.html')

    return render(request, 'registro.html')

@permission_required('las_ricuras.view_venta', raise_exception=True)
def resumen_ventas(request):
    ventas = Venta.objects.all()

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio:
        ventas = ventas.filter(fecha__date__gte=fecha_inicio)
    if fecha_fin:
        ventas = ventas.filter(fecha__date__lte=fecha_fin)

    resumen = ventas.aggregate(
        total_vendido=Sum('total'),
        cantidad_ventas=Count('id'),
    )

    contexto = {
        'total_vendido': resumen['total_vendido'] or 0,
        'cantidad_ventas': resumen['cantidad_ventas'],
        'fecha_inicio': fecha_inicio or '',
        'fecha_fin': fecha_fin or '',
    }
    return render(request, 'resumen_ventas.html', contexto)


def codigo_qr(request):
    """Genera un QR que abre el chat de WhatsApp del restaurante."""
    mensaje = "Hola, escaneé el código QR y quiero hacer un pedido"
    url_whatsapp = f"https://wa.me/573118299494?text={quote(mensaje)}"
    img = qrcode.make(url_whatsapp)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")

@login_required
def crear_pedido(request):
    platos = Plato.objects.filter(disponible=True)
    if request.method == "POST":
        mesa = request.POST.get("mesa", "")
        seleccionados = []
        for plato in platos:
            cantidad = int(request.POST.get(f"cantidad_{plato.id}", 0) or 0)
            if cantidad > 0:
                seleccionados.append((plato, cantidad))

        if not seleccionados:
            messages.error(request, "Debes seleccionar al menos un plato.")
        else:
            pedido = Pedido.objects.create(mesero=request.user, mesa=mesa)
            for plato, cantidad in seleccionados:
                DetallePedido.objects.create(pedido=pedido, plato=plato, cantidad=cantidad)
            pedido.calcular_total()
            return redirect("pedido_detalle", pedido.id)

    return render(request, "pedido_form.html", {"platos": platos})


@login_required
def pedido_detalle(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, "pedido_detalle.html", {"pedido": pedido})
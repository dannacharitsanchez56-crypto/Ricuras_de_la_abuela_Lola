from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from django.contrib.admin.views.decorators import staff_member_required
from .models import Plato, Venta, Resena
from .forms import PlatoForm, ResenaForm
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
    lista_resenas = plato.resena_set.all()
    
    prom = lista_resenas.aggregate(Avg('estrellas'))['estrellas__avg']

    mi_resena = None
    if request.user.is_authenticated:
        mi_resena = Resena.objects.filter(plato=plato, usuario=request.user).first()

    if request.method == 'POST':
        if request.user.is_authenticated:
            if mi_resena:
                form = ResenaForm(request.POST, instance=mi_resena)
            else:
                form = ResenaForm(request.POST)

            if form.is_valid():
                r = form.save(commit=False)
                r.plato = plato
                r.usuario = request.user
                r.save()
                return redirect('plato_detalle', id=plato.id)
        else:
            return redirect('login')
    else:
        if mi_resena:
            form = ResenaForm(instance=mi_resena)
        else:
            form = ResenaForm()

    contexto = {
        'plato': plato,
        'resenas': lista_resenas,
        'form': form,
        'promedio': prom,
        'mi_resena': mi_resena
    }
    return render(request, 'plato_detalle.html', contexto)


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


# --- NUEVA FUNCIÓN PARA BORRAR RESEÑA ---
@solo_staff
def eliminar_resena(request, resena_id):
    r = get_object_or_404(Resena, id=resena_id)
    plato_id = r.plato.id
    
    r.delete()
    messages.success(request, 'Reseña eliminada.')
    
    return redirect('plato_detalle', id=plato_id)
# ----------------------------------------


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


@staff_member_required
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
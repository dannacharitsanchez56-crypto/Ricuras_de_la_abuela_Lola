from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Plato, InformacionRestaurante
from .forms import InformacionRestauranteForm, AdminCrearForm, AdminEditarForm
from .decorators import solo_staff


def inicio(request):
    return render(request, 'core/inicio.html')


def historia(request):
    return render(request, 'core/historia.html')


def menu(request):
    return render(request, 'core/menu.html')


def reservas(request):
    return render(request, 'core/reservas.html')


def contacto(request):
    info = InformacionRestaurante.objects.first()
    context = {
        'info': info,
    }
    return render(request, 'core/contacto.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            siguiente = request.GET.get('next', '')
            if siguiente and url_has_allowed_host_and_scheme(siguiente, allowed_hosts={request.get_host()}):
                return redirect(siguiente)
            if user.is_staff:
                return redirect('lista_admins')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos, o el usuario está desactivado.')

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('inicio')


def registro(request):
    return render(request, 'core/registro.html')


def perfil(request):
    return render(request, 'core/perfil.html')


def lista_platos(request):
    query = request.GET.get('q', '').strip()
    platos_list = Plato.objects.filter(disponible=True)

    if query:
        platos_list = platos_list.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(categoria__icontains=query)
        )

    paginator = Paginator(platos_list, 9)
    page_number = request.GET.get('page')
    platos = paginator.get_page(page_number)

    context = {
        'platos': platos,
        'query': query,
    }
    return render(request, 'core/Platos.html', context)


def plato_detalle(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id, disponible=True)
    context = {
        'plato': plato,
    }
    return render(request, 'core/plato_detalle.html', context)


def actualizar_info(request):
    info = InformacionRestaurante.objects.first()

    if request.method == 'POST':
        form = InformacionRestauranteForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            return redirect('contacto')
    else:
        form = InformacionRestauranteForm(instance=info)

    context = {
        'form': form,
    }
    return render(request, 'core/actualizar_info.html', context)


# ---------- HU26: Gestionar usuarios administrativos ----------

@solo_staff
def lista_admins(request):
    admins = User.objects.filter(is_staff=True).order_by('username')
    return render(request, 'core/admins_lista.html', {'admins': admins})


@solo_staff
def crear_admin(request):
    if request.method == 'POST':
        form = AdminCrearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario administrativo registrado correctamente.')
            return redirect('lista_admins')
    else:
        form = AdminCrearForm()
    return render(request, 'core/admin_form.html', {'form': form, 'titulo': 'Registrar administrador'})


@solo_staff
def editar_admin(request, user_id):
    usuario = get_object_or_404(User, id=user_id, is_staff=True)
    if request.method == 'POST':
        form = AdminEditarForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos actualizados correctamente.')
            return redirect('lista_admins')
    else:
        form = AdminEditarForm(instance=usuario)
    return render(request, 'core/admin_form.html', {'form': form, 'titulo': 'Editar administrador'})


@solo_staff
def cambiar_estado_admin(request, user_id):
    usuario = get_object_or_404(User, id=user_id, is_staff=True)

    if usuario == request.user:
        messages.error(request, 'No puedes desactivarte a ti mismo.')
        return redirect('lista_admins')

    if request.method == 'POST':
        usuario.is_active = not usuario.is_active
        usuario.save()
        estado = 'activado' if usuario.is_active else 'desactivado'
        messages.success(request, f'Usuario {estado} correctamente.')
    return redirect('lista_admins')
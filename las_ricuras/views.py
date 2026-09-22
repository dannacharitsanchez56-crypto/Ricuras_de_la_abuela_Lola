from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Plato
from .forms import PlatoForm
from django.contrib.admin.views.decorators import staff_member_required


# ---------- PORTADA E INICIO ----------
def portada(request):
    return render(request, 'portada.html')


def inicio(request):
    return render(request, 'inicio.html')



# ---------- SECCIONES ----------
def menu(request):
    platos = Plato.objects.filter(disponible=True)
    return render(request, 'menu.html', {
        'platos': platos
    })





def contacto(request):
    return render(request, 'contacto.html')



def perfil(request):
    return render(request, 'perfil.html')


# ---------- PLATOS (CRUD) ----------
@staff_member_required
def Platos(request):
    platos = Plato.objects.all()
    return render(request, 'Platos.html', {'platos': platos})


def plato_detalle(request, id):
    plato = get_object_or_404(Plato, id=id)
    return render(request, 'plato_detalle.html', {'plato': plato})


@staff_member_required
def crear_plato(request):
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Platos')
    else:
        form = PlatoForm()
    return render(request, 'plato_form.html', {'form': form})


@staff_member_required
def editar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('Platos')
    else:
        form = PlatoForm(instance=plato)
    return render(request, 'plato_form.html', {
        'form': form,
        'plato': plato
    })


@staff_member_required
def eliminar_plato(request, id):
    plato = get_object_or_404(Plato, id=id)
    if request.method == 'POST':
        plato.delete()
        return redirect('Platos')
    return render(request, 'plato_confirmar_eliminar.html', {
        'plato': plato
    })


# ---------- LOGIN ----------
def login_view(request):
    return render(request, 'login.html')


# ---------- REGISTRO (con validaciones) ----------
def registro(request):
    # Si el usuario ya está logueado, lo mandamos al inicio
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # --- VALIDACIONES ---
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

        # --- CREAR USUARIO ---
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al crear la cuenta: {str(e)}')
            return render(request, 'registro.html')

    # Si es GET, mostramos el formulario vacío
    return render(request, 'registro.html')
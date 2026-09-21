from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
def portada(request):
    return render(request, 'portada.html')

def inicio(request):
    return render(request, 'inicio.html')

def menu(request):
    return render(request, 'menu.html')

def reservas(request):
    return render(request, 'reservas.html')

def Platos(request):
    return render(request, 'Platos.html')

def contacto(request):
    return render(request, 'contacto.html')

def perfil(request):
    return render(request, 'perfil.html')

# ---------- VISTA DE LOGIN ----------
# (Por ahora solo muestra el formulario; cuando quieras procesarlo, avísame)
def login_view(request):
    return render(request, 'login.html')

# ---------- VISTA DE REGISTRO ----------

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
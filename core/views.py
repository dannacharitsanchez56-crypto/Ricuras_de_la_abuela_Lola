from django.shortcuts import render

def inicio(request):
    return render(request, 'core/inicio.html')

def historia(request):
    return render(request, 'core/historia.html')

def menu(request):
    return render(request, 'core/menu.html')

def reservas(request):
    return render(request, 'core/reservas.html')

def galeria(request):
    return render(request, 'core/Platos.html')

def contacto(request):
    return render(request, 'core/contacto.html')

def login_view(request):
    return render(request, 'core/login.html')

def registro(request):
    return render(request, 'core/registro.html')

def perfil(request):
    return render(request, 'core/perfil.html')
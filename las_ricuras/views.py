from django.shortcuts import render

def inicio(request):
    return render(request, 'inicio.html')

def historia(request):
    return render(request, 'historia.html')

def menu(request):
    return render(request, 'menu.html')

def reservas(request):
    return render(request, 'reservas.html')

def Platos (request):
    return render(request, 'Platos.html')

def contacto(request):
    return render(request, 'contacto.html')

def login_view(request):
    return render(request, 'login.html')

def registro(request):
    return render(request, 'registro.html')

def perfil(request):
    return render(request, 'perfil.html')
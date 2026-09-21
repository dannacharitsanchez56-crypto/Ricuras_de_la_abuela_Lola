from django.shortcuts import render, redirect, get_object_or_404
from .models import Plato
from .forms import PlatoForm
from django.contrib.admin.views.decorators import staff_member_required



def inicio(request):
    return render(request, 'inicio.html')


def historia(request):
    return render(request, 'historia.html')

def menu(request):
    platos = Plato.objects.filter(disponible=True)

    return render(request, 'menu.html', {
        'platos': platos
    })



def reservas(request):
    return render(request, 'reservas.html')

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
        form = PlatoForm(
            request.POST,
            request.FILES,
            instance=plato
        )

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


def contacto(request):
    return render(request, 'contacto.html')


def login_view(request):
    return render(request, 'login.html')


def registro(request):
    return render(request, 'registro.html')


def perfil(request):
    return render(request, 'perfil.html')

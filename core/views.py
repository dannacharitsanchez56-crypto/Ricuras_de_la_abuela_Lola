from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Plato, InformacionRestaurante
from .forms import InformacionRestauranteForm



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
    return render(request, 'core/login.html')


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

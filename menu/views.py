from django.shortcuts import render
from las_ricuras.models import Plato


def inicio(request):
    platos = Plato.objects.all().order_by('-disponible', 'nombre')

    return render(request, 'menu/menu.html', {
        'platos': platos,
    })

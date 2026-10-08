
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def solo_staff(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        if not request.user.is_staff:
            messages.error(request, 'No tienes permisos para acceder aquí.')
            return redirect('inicio')
        return view_func(request, *args, **kwargs)
    return wrapper
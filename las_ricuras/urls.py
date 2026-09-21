from django.urls import path
from . import views

urlpatterns = [

    path('', views.inicio, name='inicio'),
    path('historia/', views.historia, name='historia'),
    path('menu/', views.menu, name='menu'),
    path('reservas/', views.reservas, name='reservas'),
    path('Platos/', views.Platos, name='Platos'),
    path('Platos/nuevo/', views.crear_plato, name='crear_plato'),
    path('Platos/<int:id>/',views.plato_detalle,name='plato_detalle'),
    path('Platos/<int:id>/editar/',views.editar_plato,name='editar_plato'),
    path('Platos/<int:id>/eliminar/',views.eliminar_plato,name='eliminar_plato'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
]

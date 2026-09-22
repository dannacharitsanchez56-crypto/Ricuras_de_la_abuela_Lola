from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('historia/', views.historia, name='historia'),
    path('menu/', views.menu, name='menu'),
    path('reservas/', views.reservas, name='reservas'),
    path('Platos/', views.lista_platos, name='Platos'),
    path('platos/<int:plato_id>/', views.plato_detalle, name='plato_detalle'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
]
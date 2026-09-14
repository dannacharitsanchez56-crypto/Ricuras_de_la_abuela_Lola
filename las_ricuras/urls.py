from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('historia/', views.historia, name='historia'),
    path('menu/', views.menu, name='menu'),
    path('reservas/', views.reservas, name='reservas'),
    path('Platos/', views.Platos, name='Platos'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
]
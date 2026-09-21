from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('', views.portada, name='portada'),
    path('inicio/', views.inicio, name='inicio'),
    path('menu/', views.menu, name='menu'),
    path('reservas/', views.reservas, name='reservas'),
    path('Platos/', views.Platos, name='Platos'),
    path('contacto/', views.contacto, name='contacto'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
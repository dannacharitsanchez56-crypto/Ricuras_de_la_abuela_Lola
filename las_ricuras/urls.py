from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    # --- Portada e Inicio ---
    path('', views.portada, name='portada'),
    path('inicio/', views.inicio, name='inicio'),
    
    # --- Autenticación ---
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),


    # --- Secciones del restaurante ---
    path('menu/', views.menu, name='menu'),
    path('contacto/', views.contacto, name='contacto'),

    # --- Platos ---
    path('Platos/', views.Platos, name='Platos'),
    path('Platos/nuevo/', views.crear_plato, name='crear_plato'),
    path('Platos/<int:id>/', views.plato_detalle, name='plato_detalle'),
    path('Platos/<int:id>/editar/', views.editar_plato, name='editar_plato'),
    path('Platos/<int:id>/eliminar/', views.eliminar_plato, name='eliminar_plato'),
]
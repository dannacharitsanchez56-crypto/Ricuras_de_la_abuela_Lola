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
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),


    path('administradores/', views.lista_admins, name='lista_admins'),
    path('administradores/nuevo/', views.crear_admin, name='crear_admin'),
    path('administradores/<int:user_id>/editar/', views.editar_admin, name='editar_admin'),
    path('administradores/<int:user_id>/estado/', views.cambiar_estado_admin, name='cambiar_estado_admin'),
]
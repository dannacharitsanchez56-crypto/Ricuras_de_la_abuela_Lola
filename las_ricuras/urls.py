from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.portada, name='portada'),
    path('inicio/', views.inicio, name='inicio'),

    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),

    path('menu/', views.menu, name='menu'),

    path('platos/', views.Platos, name='Platos'),
    path('platos/nuevo/', views.crear_plato, name='crear_plato'),
    path('platos/<int:id>/', views.plato_detalle, name='plato_detalle'),
    path('platos/<int:id>/editar/', views.editar_plato, name='editar_plato'),
    path('platos/<int:id>/eliminar/', views.eliminar_plato, name='eliminar_plato'),
    path('contacto/', views.contacto, name='contacto'),
    path('resumen-ventas/', views.resumen_ventas, name='resumen_ventas'),
]
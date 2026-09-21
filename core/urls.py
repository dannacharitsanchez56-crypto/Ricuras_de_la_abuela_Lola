from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # <--- Agrega esta línea

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('', include('las_ricuras.urls')),
]
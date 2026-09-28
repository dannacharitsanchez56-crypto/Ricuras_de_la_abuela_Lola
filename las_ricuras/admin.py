from django.contrib import admin
from .models import Plato


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'disponible')
    list_filter = ('disponible', 'categoria')
    list_editable = ('disponible',)
    search_fields = ('nombre',)

    actions = ['marcar_disponible', 'marcar_no_disponible']

    @admin.action(description='Marcar como disponible')
    def marcar_disponible(self, request, queryset):
        queryset.update(disponible=True)

    @admin.action(description='Marcar como no disponible')
    def marcar_no_disponible(self, request, queryset):
        queryset.update(disponible=False)
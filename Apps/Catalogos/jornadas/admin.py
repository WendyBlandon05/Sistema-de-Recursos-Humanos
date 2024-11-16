from django.contrib import admin
from .models import Jornada
class JornadaAdmin(admin.ModelAdmin):
    list_display = ['id_jornada', 'nombre_jornada','cantidad_horas','descripcion', 'is_active']
    search_fields = ['id_jornada', 'nombre_jornada']

admin.site.register(Jornada, JornadaAdmin)
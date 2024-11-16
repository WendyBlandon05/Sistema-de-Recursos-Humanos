from django.contrib import admin
from .models import Departamento

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['id_departamento', 'nombre_departamento', 'descripcion', 'is_active']
    search_fields = ['nombre_departamento']

admin.site.register(Departamento, DepartamentoAdmin)
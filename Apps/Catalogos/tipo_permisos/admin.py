from django.contrib import admin

# Register your models here.
from .models import Tipo_permiso

class TipoPermisoAdmin(admin.ModelAdmin):
    list_display = ['id_tipo_permisos', 'nombre_tipo_permiso','is_active']
    search_fields = ['id_tipo_permisos', 'nombre_tipo_permiso']

admin.site.register(Tipo_permiso, TipoPermisoAdmin)

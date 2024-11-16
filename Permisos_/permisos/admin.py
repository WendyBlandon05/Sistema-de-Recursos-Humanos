from django.contrib import admin

from .models import Permiso
class PermisoAdmin(admin.ModelAdmin):
    list_display = ['id_permisos', 'nombre_permiso','id_tipo_permisos','is_active']
    search_fields = ['id_permisos', 'nombre_permiso']

admin.site.register(Permiso, PermisoAdmin)
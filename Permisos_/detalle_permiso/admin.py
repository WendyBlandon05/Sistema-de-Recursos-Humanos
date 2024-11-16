
from django.contrib import admin
from .models import Detalle_permiso

class Detalle_permisoAdmin(admin.ModelAdmin):
    list_display = ['id_detalle_permisos', 'descripcion', 'fecha_inicio', 'fecha_fin', 'id_empleados','id_permisos','is_active']
    search_fields = ['id_detalle_permisos', 'id_empleados__numero_cedula']

admin.site.register(Detalle_permiso, Detalle_permisoAdmin)
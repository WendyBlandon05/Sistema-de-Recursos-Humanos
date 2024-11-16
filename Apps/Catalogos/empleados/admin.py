from django.contrib import admin

# Register your models here.
from .models import Empleado

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['id_empleados','numero_cedula', 'numero_inss','primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo', 'telefono', 'email', 'direccion', 'is_active']
    search_fields = ['numero_cedula', 'primer_nombre', 'primer_apellido', 'id_empleados', 'numero_inss']

admin.site.register(Empleado, EmpleadoAdmin)
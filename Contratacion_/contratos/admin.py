from django.contrib import admin

from .models import Contrato

class ContratoAdmin(admin.ModelAdmin):
    list_display = ['id_contratos','codigo_contrato', 'fecha_inicio', 'fecha_conclusion', 'id_tipo_contratos',
                    'id_empleados', 'id_jornada', 'id_cargos', 'id_departamento', 'is_active']
    search_fields = ['codigo_contrato', 'id_empleado__numero_cedula', 'id_tipo_contratos__nombre_tipo']


admin.site.register(Contrato, ContratoAdmin)

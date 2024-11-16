from django.contrib import admin

# Register your models here.
from Beneficios_.beneficios.models import Beneficios

class BeneficiosAdmin(admin.ModelAdmin):
    list_display = ['id_beneficios', 'nombre_beneficio', 'monto', 'descripcion', 'id_tipo_beneficios', 'is_active']
    search_fields = ['id_beneficios', 'nombre_beneficio', 'id_empleado__numero_cedula', 'is_active']


admin.site.register(Beneficios, BeneficiosAdmin)
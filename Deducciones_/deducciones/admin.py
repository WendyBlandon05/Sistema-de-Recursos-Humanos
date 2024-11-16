from django.contrib import admin

from Deducciones_.deducciones.models import Deducciones

class DeduccionesAdmin(admin.ModelAdmin):
    list_display = ['id_deducciones', 'nombre_deduccion', 'descripcion', 'monto', 'id_tipo_deducciones', 'is_active']
    search_fields = ['id_deducciones', 'nombre_deduccion']


admin.site.register(Deducciones, DeduccionesAdmin)
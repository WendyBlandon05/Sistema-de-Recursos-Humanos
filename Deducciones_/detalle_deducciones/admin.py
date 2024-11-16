from django.contrib import admin
from .models import Detalle_Deducciones

class DetalleDeduccionesAdmin(admin.ModelAdmin):
    list_display = ['id_detalle_deduciones', 'descripcion',  'id_deducciones', 'is_active']
    search_fields = ['id_detalle_deduciones', 'id_deducciones']

admin.site.register(Detalle_Deducciones, DetalleDeduccionesAdmin)
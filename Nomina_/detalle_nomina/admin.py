
from django.contrib import admin
from .models import Detalle_Nomina

class DetalleNominaAdmin(admin.ModelAdmin):
    list_display = ['id_detalle_nomina', 'id_nomina',  'is_active']
    search_fields = ['id_detalle_nomina', 'id_nomina']

admin.site.register(Detalle_Nomina, DetalleNominaAdmin)
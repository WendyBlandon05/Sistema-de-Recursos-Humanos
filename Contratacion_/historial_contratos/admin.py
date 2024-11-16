from django.contrib import admin
from .models import Historial_Contratos
class Historial_ContratosAdmin(admin.ModelAdmin):
    list_display = ['id_historial_contratos', 'id_contrato','fecha_cambio', 'is_active', 'codigo_contrato_anterior']
    search_fields = ['id_historial_contratos', 'id_contrato']

admin.site.register(Historial_Contratos, Historial_ContratosAdmin)
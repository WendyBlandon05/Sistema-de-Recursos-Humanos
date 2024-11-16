from django.contrib import admin

# Register your models here.
from .models import Tipo_contrato

class Tipo_ContratoAdmin(admin.ModelAdmin):
    list_display = ['id_tipo_contratos', 'nombre_tipo','is_active']
    search_fields = ['id_tipo_deducciones', 'nombre_tipo']

admin.site.register(Tipo_contrato, Tipo_ContratoAdmin)
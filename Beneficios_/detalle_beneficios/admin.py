from django.contrib import admin
from .models import Detalle_Beneficios

class DetalleBeneficiosAdmin(admin.ModelAdmin):
    list_display = ['id_detalle_beneficios', 'descripcion',  'id_beneficios', 'is_active']
    search_fields = ['id_detalle_beneficios', 'id_beneficios']

admin.site.register(Detalle_Beneficios, DetalleBeneficiosAdmin)
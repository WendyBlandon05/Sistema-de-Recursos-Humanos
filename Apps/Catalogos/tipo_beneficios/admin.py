from django.contrib import admin


from .models import Tipo_Beneficios

class Tipo_BeneficiosAdmin(admin.ModelAdmin):
    list_display = ['id_tipo_beneficios', 'nombre_beneficio','is_active']
    search_fields = ['id_tipo_beneficios', 'nombre_beneficio']

admin.site.register(Tipo_Beneficios, Tipo_BeneficiosAdmin)
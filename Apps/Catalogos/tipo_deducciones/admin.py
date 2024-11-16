from django.contrib import admin

# Register your models here.
from .models import Tipo_Deducciones

class Tipo_DeduccionesAdmin(admin.ModelAdmin):
    list_display = ['id_tipo_deducciones', 'nombre_tipo_deducciones','is_active']
    search_fields = ['id_tipo_deducciones', 'nombre_tipo_deducciones']

admin.site.register(Tipo_Deducciones, Tipo_DeduccionesAdmin)

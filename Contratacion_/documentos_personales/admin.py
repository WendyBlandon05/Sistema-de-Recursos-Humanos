from django.contrib import admin
from .models import documentos_personales
class documentos_personalesAdmin(admin.ModelAdmin):
    list_display = ['id_documentos_personales' ,'fecha_subida', 'id_empleados', 'id_tipo_documentos', 'is_active']
    search_fields = ['id_documentos_personales', 'id_empleados__numero_cedula']

admin.site.register(documentos_personales, documentos_personalesAdmin)
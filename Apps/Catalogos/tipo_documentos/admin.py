from django.contrib import admin

# Register your models here.
from .models import Tipo_documento

class TipodocumentoAdmin(admin.ModelAdmin):
    list_display = ['id_tipo_documentos', 'nombre_tipo_documentos','is_active']
    search_fields = ['id_tipo_documentos', 'nombre_tipo_documentos']

admin.site.register(Tipo_documento, TipodocumentoAdmin)

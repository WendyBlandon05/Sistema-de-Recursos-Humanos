from django.contrib import admin

# Register your models here.
from Apps.Catalogos.cargos.models import Cargos


class CargosAdmin(admin.ModelAdmin):

   list_display = ['id_cargos', 'nombre_cargo', 'descripcion', 'salario_base', 'is_active']
   search_fields = ['nombre_cargo']

admin.site.register(Cargos, CargosAdmin)
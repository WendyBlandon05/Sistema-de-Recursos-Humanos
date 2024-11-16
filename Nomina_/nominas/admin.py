from django.contrib import admin

from .models import Nomina
class NominaAdmin(admin.ModelAdmin):
    list_display = ['id_nomina', 'mes_pagado','total_pagar', 'fecha_pago','is_active']
    search_fields = ['id_nomina', 'mes_pagado']

admin.site.register(Nomina, NominaAdmin)
from rest_framework import serializers
from Nomina_.nominas.models import Nomina

class NominaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nomina
        fields = ['nombre_empresa','mes_pagado', 'estado','fecha_pago','total_beneficios', 'total_deducciones', 'salario_bruto', 'total_pagar' ]

        def validate_nombre_empresa(self, value):
            if len(value) < 3:
                raise serializers.ValidationError("El nombre de la empresa debe tener al menos 3 caracteres.")
            return value

        def validate_mes_pagado(self, value):
            if len(value) < 4:
                raise serializers.ValidationError("El mes debe tener al menos 4 caracteres.")
            return value

        def validate_estado(self, value):
            if len(value) < 4:
                raise serializers.ValidationError("El mes debe tener al menos 4 caracteres.")
            return value

        def validate_estado(self, value):
            if value not in ['PENDIENTE', 'PAGADA']:
                raise serializers.ValidationError("El estado debe ser PENDIENTE o PAGADA.")
            return value


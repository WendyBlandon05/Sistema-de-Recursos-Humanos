from rest_framework import serializers
from Contratacion_.contratos.models import Contrato

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = ['codigo_contrato', 'fecha_inicio', 'fecha_conclusion', 'id_tipo_contratos', 'id_empleados', 'id_jornada', 'id_cargos', 'id_departamento']

        def validate_codigo_contrato(self, value):
            if len(value) !=8:
                raise serializers.ValidationError("El código del contrato debe tener 8 caracteres")
            return value
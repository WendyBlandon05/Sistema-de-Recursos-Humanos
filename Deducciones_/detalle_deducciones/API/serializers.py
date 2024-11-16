from rest_framework import serializers
from Deducciones_.detalle_deducciones.models import Detalle_Deducciones

class Detalle_DeduccionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_Deducciones
        fields = ['descripcion', 'id_deducciones', 'id_contrato', 'is_active']

        def validate_descripcion(self, value):
            if len(value) < 10:
                raise serializers.ValidationError("La descripción debe tener al menos 10 caracteres.")
            return value
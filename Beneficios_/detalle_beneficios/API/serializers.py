from rest_framework import serializers
from Beneficios_.detalle_beneficios.models import Detalle_Beneficios

class Detalle_BeneficioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_Beneficios
        fields = ['descripcion', 'id_beneficios', 'id_contrato', 'is_active']

    def validate_descripcion(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return value


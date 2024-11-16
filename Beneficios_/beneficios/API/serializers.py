from rest_framework import serializers
from Beneficios_.beneficios.models import Beneficios

class BeneficiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficios
        fields = ['monto', 'descripcion','nombre_beneficio', 'id_tipo_beneficios', 'is_active']

    def validate_monto(self, value):
        try:
            float(value)
        except ValueError:
            raise serializers.ValidationError("El monto debe ser un número válido.")

        if value <= 0:
            raise serializers.ValidationError("El monto debe ser un valor positivo.")

        return value


    def validate_descripcion(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return value


    def validate_nombre_beneficio(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("El nombre del beneficio debe tener al menos 4 caracteres.")
        return value


from rest_framework import serializers
from Deducciones_.deducciones.models import Deducciones

class DeduccionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deducciones
        fields = ['monto', 'nombre_deduccion', 'descripcion', 'id_tipo_deducciones']



    def validate_descripcion(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return value


    def validate_nombre_deduccion(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("El nombre de la deduccion debe tener al menos 4 caracteres.")
        return value

    def validate_monto(self, value):
        try:
            float(value)
        except ValueError:
            raise serializers.ValidationError("El monto debe ser un número válido.")

        if value <= 0:
            raise serializers.ValidationError("El monto debe ser un valor positivo.")

        return value
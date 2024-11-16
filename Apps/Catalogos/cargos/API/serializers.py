from rest_framework import serializers
from Apps.Catalogos.cargos.models import Cargos

class CargosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargos
        fields = ['nombre_cargo', 'descripcion','salario_base', 'is_active']

    def validate_nombre_cargo(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre del tipo del cargo debe tener al menos 3 letras.")
        return value

    def validate_descripcion(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("La descripción del cargo debe tener al menos 10 letras.")
        return value

    def validate_salario_base(self, value):
        try:
            salario = float(value)
        except ValueError:
            raise serializers.ValidationError("El salario base debe ser un número válido.")

        if salario <= 0:
            raise serializers.ValidationError("El salario base debe ser un valor positivo.")

        if salario < 5500:
            raise serializers.ValidationError("El salario base debe ser mayor a 5500.")
        return salario
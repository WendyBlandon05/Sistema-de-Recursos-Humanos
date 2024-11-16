from rest_framework import serializers
from Apps.Catalogos.departamentos.models import Departamento

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['nombre_departamento', 'descripcion']


    def validate_descripcion(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return value


    def validate_nombre_departamento(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("El nombre del departamento debe tener al menos 4 caracteres.")
        return value
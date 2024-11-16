from rest_framework import serializers
from Apps.Catalogos.jornadas.models import Jornada

class JornadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jornada
        fields = ['id_jornada','nombre_jornada','cantidad_horas', 'descripcion']

    def validate_descripcion(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return value


    def validate_nombre_jornada(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("El nombre de la jornada debe tener al menos 4 caracteres.")
        return value

    def validate_cantidad_horas(self, value):
        if value < 90 or value > 300:
            raise serializers.ValidationError("La cantidad de horas debe estar entre 90 y 300.")
        return value
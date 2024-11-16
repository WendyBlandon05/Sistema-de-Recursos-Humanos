from rest_framework import serializers
from Apps.Catalogos.tipo_deducciones.models import Tipo_Deducciones

class Tipo_DeduccionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Deducciones
        fields = ['nombre_tipo_deducciones']


    def validate_nombre_tipo_deducciones(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre del tipo de deducción debe tener al menos 3 caracteres.")
        return value
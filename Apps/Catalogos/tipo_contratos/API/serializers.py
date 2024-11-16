from rest_framework import serializers
from Apps.Catalogos.tipo_contratos.models import Tipo_contrato

class Tipo_ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_contrato
        fields = ['nombre_tipo']

    def validate_nombre_tipo(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre del tipo de contrato debe tener al menos 3 caracteres.")
        return value
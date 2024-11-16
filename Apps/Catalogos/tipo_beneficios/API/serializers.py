from rest_framework import serializers
from Apps.Catalogos.tipo_beneficios.models import Tipo_Beneficios

class Tipo_BeneficiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Beneficios
        fields =['nombre_beneficio']

    def validate_nombre_beneficio(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre del tipo de beneficio debe tener al menos 3 caracteres.")
        return value
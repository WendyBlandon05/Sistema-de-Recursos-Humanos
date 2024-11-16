from rest_framework import serializers
from Apps.Catalogos.tipo_documentos.models import Tipo_documento

class Tipo_DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_documento
        fields = ['nombre_tipo_documentos']

    def validate_nombre_tipo_documentos(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre del tipo de documento debe tener al menos 3 caracteres.")
        return value
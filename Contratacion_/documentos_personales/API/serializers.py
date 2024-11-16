from rest_framework import serializers
from Contratacion_.documentos_personales.models import documentos_personales

class Documentos_PersonalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = documentos_personales
        fields = [ 'fecha_subida', 'archivo','id_empleados', 'id_tipo_documentos']
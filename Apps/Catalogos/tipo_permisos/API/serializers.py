from rest_framework import serializers
from Apps.Catalogos.tipo_permisos.models import Tipo_permiso

class TipoPermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_permiso
        fields = ['nombre_tipo_permiso']

    def validate_nombre_tipo_permiso(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return value
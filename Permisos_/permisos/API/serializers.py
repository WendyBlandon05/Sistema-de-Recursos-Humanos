from rest_framework import serializers
from Permisos_.permisos.models import Permiso

class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = ['nombre_permiso', 'id_tipo_permisos']

    def validate_nombre_permiso(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("El nombre del permiso debe tener al menos 4 caracteres.")
        return value
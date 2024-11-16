from rest_framework import serializers
from Permisos_.detalle_permiso.models import Detalle_permiso

class Detalle_PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_permiso
        fields = ['descripcion', 'fecha_inicio', 'fecha_fin', 'id_empleados', 'id_permisos']

        def validate_descripcion(self, value):
            if len(value) < 10:
                raise serializers.ValidationError("La descripción debe tener al menos 10 caracteres.")
            return value
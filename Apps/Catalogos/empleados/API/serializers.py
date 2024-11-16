from rest_framework import serializers
from Apps.Catalogos.empleados.models import Empleado
import re

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['id_empleados','numero_cedula', 'numero_inss', 'primer_nombre', 'segundo_nombre', 'primer_apellido',
              'segundo_apellido',
              'direccion',
              'sexo',
              'telefono',
              'email', 'estado']


    def validate_numero_cedula(self, value):
        if not re.match(r'^\d{14}[A-Za-z]$', value):
            raise serializers.ValidationError("Error al digitar la cédula de identidad, revisa por favor.")
        return value

    def validate_email(self, value):
        if "@" not in value:
            raise serializers.ValidationError("Verifique su correo.")
        return value


    def validate_numero_inss(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El número de INSS debe contener solo dígitos.")
        if len(value) != 9:
            raise serializers.ValidationError("El número de INSS debe tener 9 dígitos.")
        return value


    def validate_primer_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El primer nombre debe tener al menos 3 caracteres.")
        return value


    def validate_segundo_nombre(self, value):
        if value and len(value) < 3:
            raise serializers.ValidationError("El segundo nombre debe tener al menos 3 caracteres.")
        return value


    def validate_primer_apellido(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("El primer apellido debe tener al menos 2 caracteres.")
        return value

    def validate_segundo_apellido(self, value):
        if value and len(value) < 2:
            raise serializers.ValidationError("El segundo apellido debe tener al menos 2 caracteres.")
        return value


    def validate_telefono(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El número de teléfono debe contener solo dígitos.")
        if len(value) < 8:
            raise serializers.ValidationError("El número de teléfono debe tener al menos 8 dígitos.")
        return value
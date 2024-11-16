
from rest_framework import serializers
from Contratacion_.historial_contratos.models import Historial_Contratos

class Historial_ContratosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historial_Contratos
        fields = '__all__'

        #['id_contrato', 'fecha_cambio', 'codigo_contrato_anterior']
from rest_framework import serializers
from Nomina_.detalle_nomina.models import Detalle_Nomina

class Detalle_NominaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Detalle_Nomina
        fields = ['id_nomina', 'id_contrato','salario_bruto', 'salario_neto', 'monto_beneficios','monto_deducciones']
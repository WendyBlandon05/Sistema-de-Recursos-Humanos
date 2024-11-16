from django.db import models

from Contratacion_.contratos.models import Contrato
from Nomina_.nominas.models import Nomina

class Detalle_Nomina(models.Model):
    id_detalle_nomina = models.AutoField(primary_key=True)
    id_nomina = models.ForeignKey(Nomina, on_delete= models.CASCADE)
    id_contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    salario_bruto = models.DecimalField(max_digits=10, decimal_places=2, null=False, default= 0)
    salario_neto = models.DecimalField(max_digits=10, decimal_places=2, null=False, default= 0)
    monto_beneficios = models.DecimalField(max_digits=10, decimal_places=2, null=False, default= 0)
    monto_deducciones = models.DecimalField(max_digits=10, decimal_places=2, null=False, default= 0)

    is_active = models.BooleanField(default=True)
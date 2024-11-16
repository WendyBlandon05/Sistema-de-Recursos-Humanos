from django.db import models

from Contratacion_.contratos.models import Contrato
from Deducciones_.deducciones.models import Deducciones

class Detalle_Deducciones(models.Model):
    id_detalle_deduciones = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    id_contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    id_deducciones = models.ForeignKey(Deducciones, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

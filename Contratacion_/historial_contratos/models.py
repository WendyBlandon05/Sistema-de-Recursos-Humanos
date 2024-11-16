from django.db import models
from Contratacion_.contratos.models import Contrato
# Create your models here.
class Historial_Contratos(models.Model):
    id_historial_contratos = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    fecha_cambio = models.DateTimeField()
    codigo_contrato_anterior = models.CharField(max_length=8)
    is_active = models.BooleanField(default=True)
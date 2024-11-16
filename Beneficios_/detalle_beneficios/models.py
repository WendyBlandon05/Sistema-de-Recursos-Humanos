from django.db import models
from Beneficios_.beneficios.models import Beneficios
from Contratacion_.contratos.models import Contrato

class Detalle_Beneficios(models.Model):
    id_detalle_beneficios = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length=50)
    id_contrato = models.ForeignKey(Contrato,related_name='detalle_beneficios', on_delete=models.CASCADE)
    id_beneficios = models.ForeignKey(Beneficios, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.id_detalle_beneficios}"
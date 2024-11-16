from django.db import models
from Apps.Catalogos.tipo_beneficios.models import Tipo_Beneficios
# Create your models here.
class Beneficios(models.Model):
    id_beneficios = models.AutoField(primary_key = True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=50)
    nombre_beneficio = models.CharField(max_length= 20)
    id_tipo_beneficios = models.ForeignKey(Tipo_Beneficios, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
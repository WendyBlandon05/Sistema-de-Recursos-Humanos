from django.db import models
from Apps.Catalogos.tipo_deducciones.models import Tipo_Deducciones
# Create your models here.
class Deducciones(models.Model):
    id_deducciones = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_deduccion = models.CharField(max_length= 20)
    descripcion = models.CharField(max_length=50)
    id_tipo_deducciones = models.ForeignKey(Tipo_Deducciones, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_deducciones}"
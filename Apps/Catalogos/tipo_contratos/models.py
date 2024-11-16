from django.db import models

# Create your models here.
#
class Tipo_contrato(models.Model):
    id_tipo_contratos = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.id_tipo_contratos}"
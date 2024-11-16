from django.db import models

# Create your models here.
class Tipo_Deducciones(models.Model):
    id_tipo_deducciones = models.AutoField(primary_key=True)
    nombre_tipo_deducciones = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
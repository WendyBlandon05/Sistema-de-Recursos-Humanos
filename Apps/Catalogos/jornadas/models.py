from django.db import models

# Create your models here.
class Jornada(models.Model):
    id_jornada =  models.AutoField(primary_key=True)
    nombre_jornada = models.CharField(max_length= 50)
    cantidad_horas = models.IntegerField()
    descripcion = models.CharField(max_length= 150)
    is_active = models.BooleanField(default=True)
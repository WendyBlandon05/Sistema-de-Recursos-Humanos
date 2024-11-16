from django.db import models

from Apps.Catalogos.empleados.models import Empleado
from Permisos_.permisos.models import Permiso

# Create your models here.
class Detalle_permiso (models.Model):
    id_detalle_permisos = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length= 200)
    fecha_inicio = models.DateTimeField(null=False)
    fecha_fin = models.DateTimeField(null=False)
    id_empleados = models.ForeignKey(Empleado, on_delete= models.CASCADE, db_column= 'id_empleados')
    id_permisos = models.ForeignKey(Permiso, on_delete= models.CASCADE, db_column= 'id_permisos')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.descripcion
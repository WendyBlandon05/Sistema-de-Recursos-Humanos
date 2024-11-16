from django.db import models
from Apps.Catalogos.tipo_permisos.models import Tipo_permiso

class Permiso(models.Model):
    id_permisos = models.AutoField(primary_key=True)
    nombre_permiso = models.CharField(max_length= 50)
    id_tipo_permisos = models.ForeignKey(Tipo_permiso, on_delete= models.CASCADE, db_column= 'id_tipo_permisos')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_permisos}"
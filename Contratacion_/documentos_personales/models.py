from django.core.files.storage import FileSystemStorage
from django.db import models
from Apps.Catalogos.empleados.models import Empleado
from Apps.Catalogos.tipo_documentos.models import Tipo_documento

# Create your models here.
class documentos_personales(models.Model):
    id_documentos_personales = models.AutoField(primary_key = True)
    archivo = models.FileField(upload_to='documentos_personales/', storage=FileSystemStorage(location="C:/Admin_RH_Documentos/"))
    fecha_subida = models.DateTimeField(auto_now_add=True)
    id_empleados = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column= 'id_empleados')
    id_tipo_documentos = models.ForeignKey(Tipo_documento, on_delete=models.CASCADE, db_column= 'id_tipo_documentos')
    is_active = models.BooleanField(default=True)

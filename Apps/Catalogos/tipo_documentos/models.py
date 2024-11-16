from django.db import models

# Create your models here.
class Tipo_documento(models.Model):
    id_tipo_documentos = models.AutoField(primary_key=True)
    nombre_tipo_documentos = models.CharField(max_length= 50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id_tipo_documentos)
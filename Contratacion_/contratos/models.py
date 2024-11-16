from django.db import models

from Apps.Catalogos.cargos.models import Cargos
from Apps.Catalogos.jornadas.models import Jornada
from Apps.Catalogos.tipo_contratos.models import Tipo_contrato
from Apps.Catalogos.empleados.models import Empleado
from Apps.Catalogos.departamentos.models import Departamento

# Create your models here.
class Contrato(models.Model):
    id_contratos = models.AutoField(primary_key=True)
    codigo_contrato = models.CharField(max_length=8)
    fecha_inicio = models.DateTimeField(null = False)
    fecha_conclusion = models.DateTimeField(null = False)
    id_tipo_contratos = models.ForeignKey(Tipo_contrato, on_delete=models.CASCADE, db_column= 'id_tipo_contratos')
    id_empleados = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    id_jornada = models.ForeignKey(Jornada, on_delete= models.CASCADE)
    id_cargos = models.ForeignKey(Cargos, on_delete= models.CASCADE)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_contratos}"
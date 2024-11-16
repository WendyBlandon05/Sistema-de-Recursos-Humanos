from django.db import models


class Cargos(models.Model):
    id_cargos = models.AutoField(primary_key=True)
    nombre_cargo = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=255, null=False)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_cargos}"
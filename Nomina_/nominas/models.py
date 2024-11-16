from django.db import models

# Create your models here.
class Nomina(models.Model):
    id_nomina = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=20, null=True)
    mes_pagado = models.CharField(max_length= 20)#VALIDAR NONINA POR MES
    estado = models.CharField(max_length=20, choices=[('PENDIENTE', 'Pendiente'), ('PAGADA', 'Pagada')])
    fecha_pago = models.DateField()
    total_beneficios = models.DecimalField(max_digits=20, decimal_places=2, null=False, default=0)
    total_deducciones = models.DecimalField(max_digits=20, decimal_places=2, null=False, default=0)
    salario_bruto = models.DecimalField(max_digits=20, decimal_places=2, null=False, default= 0)
    total_pagar = models.DecimalField(max_digits=20, decimal_places=2)
    is_active = models.BooleanField(default=True)


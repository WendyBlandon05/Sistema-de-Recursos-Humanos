from django.db import models

class Empleado (models.Model):
    #Opciones de genero
    SEXO_OPCIONES = [('M', 'Hombre'), ('F', 'Mujer'), ]
    id_empleados = models.AutoField(primary_key = True)
    numero_cedula = models.CharField(max_length= 16)
    numero_inss = models.CharField(max_length= 11)
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=SEXO_OPCIONES, default='F')
    telefono =models.CharField(max_length=13)
    email = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_empleados}"

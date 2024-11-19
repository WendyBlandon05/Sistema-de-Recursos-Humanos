from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Usuario(AbstractUser):

    cedula_validator = RegexValidator(regex=r'^\d{14}$', message="El número de cédula debe tener 14 dígitos.")

    class Meta:
        db_table = 'Usuario'
# Generated by Django 4.1 on 2024-11-09 01:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0002_usuario_numero_cedula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='numero_cedula',
            field=models.CharField(default='WEI12345678142', max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message='El número de cédula debe tener 14 dígitos.', regex='^\\d{14}$')]),
            preserve_default=False,
        ),
    ]
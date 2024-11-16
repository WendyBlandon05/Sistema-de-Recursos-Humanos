# Generated by Django 4.1 on 2024-11-09 01:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='numero_cedula',
            field=models.CharField(max_length=14, null=True, validators=[django.core.validators.RegexValidator(message='El número de cédula debe tener 14 dígitos.', regex='^\\d{14}$')]),
        ),
    ]

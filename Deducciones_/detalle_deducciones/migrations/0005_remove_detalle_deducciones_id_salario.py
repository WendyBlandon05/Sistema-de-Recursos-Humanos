# Generated by Django 4.1 on 2024-11-06 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detalle_deducciones', '0004_detalle_deducciones_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalle_deducciones',
            name='id_salario',
        ),
    ]

# Generated by Django 4.2.16 on 2024-10-16 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detalle_deducciones', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalle_deducciones',
            name='id_tipo_deducciones',
        ),
    ]

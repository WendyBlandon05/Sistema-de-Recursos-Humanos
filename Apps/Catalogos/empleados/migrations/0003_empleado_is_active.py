# Generated by Django 4.1 on 2024-10-27 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0002_empleado_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

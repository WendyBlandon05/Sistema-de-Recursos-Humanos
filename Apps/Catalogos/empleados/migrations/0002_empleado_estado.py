# Generated by Django 4.2.16 on 2024-10-17 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]

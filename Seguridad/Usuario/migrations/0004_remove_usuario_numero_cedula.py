# Generated by Django 4.1 on 2024-11-09 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuario', '0003_alter_usuario_numero_cedula'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='numero_cedula',
        ),
    ]

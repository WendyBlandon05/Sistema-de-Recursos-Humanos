# Generated by Django 4.2.16 on 2024-10-15 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_contrato',
            fields=[
                ('id_tipo_contratos', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo', models.CharField(max_length=50)),
            ],
        ),
    ]

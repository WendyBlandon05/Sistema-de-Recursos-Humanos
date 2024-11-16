# Generated by Django 4.2.16 on 2024-10-15 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nomina',
            fields=[
                ('id_nomina', models.AutoField(primary_key=True, serialize=False)),
                ('mes_pagado', models.CharField(max_length=20)),
                ('total_pagar', models.DecimalField(decimal_places=2, max_digits=20)),
                ('fecha_pago', models.DateField()),
            ],
        ),
    ]

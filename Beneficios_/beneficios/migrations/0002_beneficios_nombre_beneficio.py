# Generated by Django 4.2.16 on 2024-10-17 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficios',
            name='nombre_beneficio',
            field=models.CharField(default='PRUEBA', max_length=20),
            preserve_default=False,
        ),
    ]

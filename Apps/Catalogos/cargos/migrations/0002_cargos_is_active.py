# Generated by Django 4.1 on 2024-10-27 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargos',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

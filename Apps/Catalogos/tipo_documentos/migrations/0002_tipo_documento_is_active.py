# Generated by Django 4.1 on 2024-10-26 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipo_documentos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipo_documento',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
# Generated by Django 4.2.16 on 2024-10-16 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beneficios', '0001_initial'),
        ('detalle_beneficios', '0002_remove_detalle_beneficios_id_tipo_beneficios'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle_beneficios',
            name='id_beneficios',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='beneficios.beneficios'),
            preserve_default=False,
        ),
    ]
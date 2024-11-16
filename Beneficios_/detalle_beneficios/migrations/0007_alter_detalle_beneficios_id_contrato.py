# Generated by Django 4.1 on 2024-11-12 04:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0004_remove_contrato_id_nomina'),
        ('detalle_beneficios', '0006_detalle_beneficios_id_contrato'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle_beneficios',
            name='id_contrato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalle_beneficios', to='contratos.contrato'),
        ),
    ]

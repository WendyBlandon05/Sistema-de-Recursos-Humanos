# Generated by Django 4.2.16 on 2024-10-16 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deducciones', '0001_initial'),
        ('detalle_deducciones', '0002_remove_detalle_deducciones_id_tipo_deducciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle_deducciones',
            name='id_deducciones',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='deducciones.deducciones'),
            preserve_default=False,
        ),
    ]

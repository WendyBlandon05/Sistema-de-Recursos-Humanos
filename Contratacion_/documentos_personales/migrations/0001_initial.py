# Generated by Django 4.2.16 on 2024-10-15 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empleados', '0001_initial'),
        ('tipo_documentos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='documentos_personales',
            fields=[
                ('id_documentos_personales', models.AutoField(primary_key=True, serialize=False)),
                ('direccion_archivo', models.CharField(max_length=100)),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('id_empleados', models.ForeignKey(db_column='id_empleados', on_delete=django.db.models.deletion.CASCADE, to='empleados.empleado')),
                ('id_tipo_documentos', models.ForeignKey(db_column='id_tipo_documentos', on_delete=django.db.models.deletion.CASCADE, to='tipo_documentos.tipo_documento')),
            ],
        ),
    ]

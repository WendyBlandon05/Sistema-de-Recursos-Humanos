# Generated by Django 4.2.16 on 2024-10-15 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empleados', '0001_initial'),
        ('tipo_contratos', '0001_initial'),
        ('cargos', '0001_initial'),
        ('jornadas', '0001_initial'),
        ('departamentos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id_contratos', models.AutoField(primary_key=True, serialize=False)),
                ('codigo_contrato', models.CharField(max_length=8)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_conclusion', models.DateTimeField()),
                ('id_cargos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cargos.cargos')),
                ('id_departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='departamentos.departamento')),
                ('id_empleados', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empleados.empleado')),
                ('id_jornada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jornadas.jornada')),
                ('id_tipo_contratos', models.ForeignKey(db_column='id_tipo_contratos', on_delete=django.db.models.deletion.CASCADE, to='tipo_contratos.tipo_contrato')),
            ],
        ),
    ]

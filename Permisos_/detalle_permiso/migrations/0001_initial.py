# Generated by Django 4.2.16 on 2024-10-15 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empleados', '0001_initial'),
        ('permisos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detalle_permiso',
            fields=[
                ('id_detalle_permisos', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=200)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('id_empleados', models.ForeignKey(db_column='id_empleados', on_delete=django.db.models.deletion.CASCADE, to='empleados.empleado')),
                ('id_permisos', models.ForeignKey(db_column='id_permisos', on_delete=django.db.models.deletion.CASCADE, to='permisos.permiso')),
            ],
        ),
    ]
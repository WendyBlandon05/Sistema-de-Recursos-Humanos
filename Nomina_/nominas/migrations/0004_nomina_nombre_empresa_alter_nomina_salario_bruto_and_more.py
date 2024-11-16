# Generated by Django 4.1 on 2024-11-11 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nominas', '0003_nomina_salario_bruto_nomina_total_beneficios_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomina',
            name='nombre_empresa',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='nomina',
            name='salario_bruto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='nomina',
            name='total_beneficios',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='nomina',
            name='total_deducciones',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
# Generated by Django 3.2.9 on 2021-11-26 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_remove_employee_is_active'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='complete_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='packer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='packer', to='staff.employee'),
        ),
        migrations.AlterField(
            model_name='order',
            name='printer_operator',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='printer_operator', to='staff.employee'),
        ),
        migrations.AlterField(
            model_name='order',
            name='production_site',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='staff.productionsite'),
        ),
    ]

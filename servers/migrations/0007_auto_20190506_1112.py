# Generated by Django 2.2 on 2019-05-06 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0006_auto_20190430_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='comparison_value',
            field=models.FloatField(help_text='Either in % or in GB for disk space or in minutes for downtime', verbose_name='Value'),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='data_type',
            field=models.IntegerField(choices=[(0, 'CPU_USAGE'), (1, 'MEMORY_USAGE'), (2, 'DISK_SPACE_LEFT'), (3, 'DOWNTIME')], verbose_name='Data Type'),
        ),
        migrations.AlterField(
            model_name='devicedata',
            name='data_type',
            field=models.IntegerField(choices=[(0, 'CPU_USAGE'), (1, 'MEMORY_USAGE'), (2, 'DISK_SPACE_LEFT'), (3, 'DOWNTIME')], verbose_name='Data Type'),
        ),
    ]

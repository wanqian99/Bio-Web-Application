# Generated by Django 3.0.3 on 2022-05-05 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genedata', '0005_auto_20220505_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protein',
            name='sequence',
            field=models.CharField(max_length=40000),
        ),
    ]

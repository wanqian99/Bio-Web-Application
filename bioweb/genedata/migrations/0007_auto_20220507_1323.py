# Generated by Django 3.0.3 on 2022-05-07 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('genedata', '0006_auto_20220505_0754'),
    ]

    operations = [
        migrations.RenameField(
            model_name='protein',
            old_name='taxanomy',
            new_name='taxonomy',
        ),
        migrations.AlterField(
            model_name='taxonomy_domain',
            name='pfam_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='genedata.Pfam'),
        ),
    ]

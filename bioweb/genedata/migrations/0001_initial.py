# Generated by Django 3.0.3 on 2022-05-05 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('taxa_id', models.IntegerField(primary_key=True, serialize=False)),
                ('clade', models.CharField(default='E', max_length=1)),
                ('genus', models.CharField(max_length=256)),
                ('species', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Protein',
            fields=[
                ('protein_id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('sequence', models.CharField(max_length=40000)),
                ('length', models.IntegerField()),
                ('taxanomy', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='genedata.Taxonomy')),
            ],
        ),
    ]

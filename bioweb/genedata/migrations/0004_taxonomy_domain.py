# Generated by Django 3.0.3 on 2022-05-05 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('genedata', '0003_taxonomy_protein'),
    ]

    operations = [
        migrations.CreateModel(
            name='Taxonomy_Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pfam_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='genedata.Protein')),
                ('taxa_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='genedata.Taxonomy')),
            ],
        ),
    ]
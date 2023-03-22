# Generated by Django 3.0.3 on 2022-05-05 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('genedata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pfam',
            fields=[
                ('domain_id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('domain_description', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Domains',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=256)),
                ('start', models.IntegerField()),
                ('stop', models.IntegerField()),
                ('pfam_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genedata.Pfam')),
                ('protein_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genedata.Protein')),
            ],
        ),
    ]
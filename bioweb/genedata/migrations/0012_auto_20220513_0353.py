# Generated by Django 3.0.3 on 2022-05-13 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genedata', '0011_auto_20220509_0353'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Taxonomy_Domain',
            new_name='Taxonomy_Pfam',
        ),
    ]

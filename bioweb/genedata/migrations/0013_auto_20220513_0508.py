# Generated by Django 3.0.3 on 2022-05-13 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genedata', '0012_auto_20220513_0353'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Taxonomy_Pfam',
            new_name='Taxonomy_Domain',
        ),
    ]
import factory
from random import randint
from .models import *

# taxonomy model factory
class Taxonomy_Factory(factory.django.DjangoModelFactory):
    # initialize sample values for the fields
    taxa_id = 53326
    clade = "E"
    genus = "Ancylostoma"
    species = "ceylanicum"

    # define model
    class Meta:
        model = Taxonomy



class Protein_Factory(factory.django.DjangoModelFactory):
    # initialize sample values for the fields
    protein_id = "A0A016S8J7"
    sequence = "MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA"
    length = len(sequence)
    # foreign key, link it to Taxonomy_Factory
    taxonomy = factory.SubFactory(Taxonomy_Factory)

    # define model
    class Meta:
        model = Protein



class Domains_Factory(factory.django.DjangoModelFactory):
    # initialize sample values for the fields
    pfam_id = 'PF01650'
    description = 'Peptidase C13 legumain'
    start = randint(1,10000)
    stop = start + randint(1,10000)
    # foreign key, link it to Protein_Factory
    protein_id = factory.SubFactory(Protein_Factory)

    # define model
    class Meta:
        model = Domains



class Pfam_Factory(factory.django.DjangoModelFactory):
    # initialize sample values for the fields
    domain_id = "PF01650"
    domain_description = "PeptidaseC13family"

    # define model
    class Meta:
        model = Pfam


class Taxonomy_Pfam_Factory(factory.django.DjangoModelFactory):
    # initialize sample values for the fields
    taxa_id = 53326
    # fk
    # taxonomy = factory.SubFactory(Taxonomy_Factory)

    # foreign key, link it to Protein_Factory
    protein_id = factory.SubFactory(Protein_Factory)

    # define model
    class Meta:
            model = Taxonomy_Pfam



class Taxonomy_Protein_Factory(factory.django.DjangoModelFactory):
    # initialize sample values for the fields
    taxa_id = 53326
    # fk
    # taxonomy = factory.SubFactory(Taxonomy_Factory)

    # foreign key, link it to Pfam_Factory
    pfam_id = factory.SubFactory(Pfam_Factory)

    # define model
    class Meta:
            model = Taxonomy_Protein
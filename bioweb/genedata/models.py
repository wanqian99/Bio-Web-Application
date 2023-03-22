from django.db import models

# Create your models here.

# Organism/ Taxonomy table model
# Organisms have many proteins, have a genus name, have a species name
class Taxonomy(models.Model):
    # primary key for taxonomy model
    taxa_id = models.IntegerField(primary_key=True, null=False, blank=False)

    # clade column in assignment_data_set.csv has a default value of 'E'
    clade = models.CharField(max_length=1, default='E', null=False, blank=False)

    # genus field
    genus = models.CharField(max_length=256, null=False, blank=False)

    # species field
    species = models.CharField(max_length=256, null=False, blank=False)

    # return the string value in the taxa_id primary key
    def __str__(self):
        return self.taxa_id



# Protein table model
# Proteins have many domains, have 1 sequence
class Protein(models.Model):
    # primary key for protein model
    protein_id = models.CharField(primary_key=True, max_length=256, null=False, blank=False)

    # longest sequence is less than 40,000 characters long
    sequence = models.CharField(max_length=40000, null=False, blank=False)

    # length field
    length = models.IntegerField(null=False, blank=False)

    # foreign key referenced from Taxonomy model
    # taxonomy record will remain even if we delete Protein record
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.DO_NOTHING, related_name='taxa_in_protein')

    # return the string value in the protein_id primary key
    def __str__(self):
        return self.protein_id



# Pfam table model
class Pfam(models.Model):
    # primary key for pfam model
    domain_id = models.CharField(primary_key=True, max_length=256, null=False, blank=False)

    # domain_description field
    domain_description = models.CharField(max_length=256, null=False, blank=False)

    # return the string value in the domain_id primary key
    def __str__(self):
        return self.domain_id



# Domains table model
# Domains have 1 pfam id
class Domains(models.Model):
    # foreign key referenced from Pfam model
    # pfam_id record will be removed if we delete Domains record
    pfam_id = models.ForeignKey(Pfam, on_delete=models.CASCADE, related_name='pfamid_in_domains')

    # description field
    description = models.CharField(max_length=256, null=False, blank=False)

    # start field
    start = models.IntegerField(null=False, blank=False)

    # stop field
    stop = models.IntegerField(null=False, blank=False)

    # foreign key referenced from Protein model
    # protein_id record will be removed if we delete Domains record
    protein_id = models.ForeignKey(Protein, on_delete=models.CASCADE, related_name='domains')

    # return the string value in the pfam_id primary key
    def __str__(self):
        return self.pfam_id



# Taxanomy and Protein linking table model
class Taxonomy_Protein(models.Model):
    # foreign key referenced from Taxonomy model
    # taxa_id record will remain even if we delete Taxonomy_Protein record
    taxa_id = models.ForeignKey(Taxonomy, on_delete=models.DO_NOTHING)

    # foreign key referenced from Protein model
    # protein_id record will remain even if we delete Taxonomy_Protein record
    protein_id = models.ForeignKey(Protein, on_delete=models.DO_NOTHING)

    # return the string value in the taxa_id key
    def __str__(self):
        return self.taxa_id



# Taxanomy and Pfam linking table model
class Taxonomy_Pfam(models.Model):
    # foreign key referenced from Taxonomy model
    # taxa_id record will remain even if we delete Taxonomy_Domain record
    taxa_id = models.ForeignKey(Taxonomy, on_delete=models.DO_NOTHING)
    
    # foreign key referenced from pfam model
    # pfam_id record will remain even if we delete Taxonomy_Domain record
    pfam_id = models.ForeignKey(Pfam, on_delete=models.DO_NOTHING)

    # return the string value in the taxa_id key
    def __str__(self):
        return self.taxa_id
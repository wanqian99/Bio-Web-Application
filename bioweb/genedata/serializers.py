from rest_framework import serializers
from .models import *
    

# taxonomy serializer
class TaxonomySerializer(serializers.ModelSerializer):
    # define model and fields
    class Meta:
        model = Taxonomy
        fields = ['taxa_id', 'clade', 'genus', 'species']



# create serializer
class CreateProteinSerializer(serializers.ModelSerializer):
    # taxonomy is an fk in protein model
    taxonomy = TaxonomySerializer()
    # define model and fields
    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'length', 'taxonomy']

    # create a method to get the taxonomy fk data
    # this displays the domain_id and domain_description in the Pfam model, 
    # that is related to the fk in Domain model
    def create(self, validated_data):
        # get taxonomy data that the user provides
        taxonomy_data = self.initial_data.get('taxonomy')
        # use a python dict, to store the key value pairs to override the taxonomy field
        # get the pk from Taxonomy and validate it with taxonomy_data['taxa_id']
        protein = Protein(**{**validated_data, 
                            'taxonomy' : Taxonomy.objects.get(pk = taxonomy_data['taxa_id'])
                        })
        protein.save()
        return protein



# pfam serializer
class PfamSerializer(serializers.ModelSerializer):
    # define model and fields
    class Meta:
        model = Pfam
        fields = ['domain_id', 'domain_description']



# domain serializer
class DomainSerializer(serializers.ModelSerializer):
    # used to get pfam_id data as it is a fk
    pfam_id = PfamSerializer()
    # define model and fields
    class Meta:
        model = Domains
        fields = ['pfam_id', 'description', 'start', 'stop']

    # create a method to get the pfam_id fk data
    # this displays the domain_id and domain_description in the Pfam model, 
    # that is related to the fk in Domain model
    def create(self, validated_data):
        pfam_data = self.initial_data.get('pfam_id')
        # use a python dict, to store the key value pairs to override the pfam_id field
        # get the pk from Pfam and validate it with pfam_data['domain_id']
        domain = Domains(**{**validated_data, 
                            'pfam_id' : Pfam.objects.get(pk = pfam_data['domain_id'])
                        })
        domain.save()
        return domain



# protein serializer
class ProteinSerializer(serializers.ModelSerializer):
    # used to get taxonomy data as it is a fk
    taxonomy = TaxonomySerializer()
    # domains table is not included in protein model
    domains = DomainSerializer(many=True)
    # define model and fields
    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxonomy', 'length', 'domains']
    
    # create a method to get the taxonomy fk data
    # this displays the taxa_id, clade, genus, species in the Taxonomy model, 
    # that is related to the fk in Protein model
    def create(self, validated_data):
        taxonomy_data = self.initial_data.get('taxonomy')
        # use a python dict, to store the key value pairs to override the taxonomy field
        # get the pk from Taxonomy and validate it with taxonomy_data['taxa_id']
        protein = Protein(**{**validated_data, 
                            'taxonomy' : Taxonomy.objects.get(pk = taxonomy_data['taxa_id'])
                         })
        protein.save()
        return protein
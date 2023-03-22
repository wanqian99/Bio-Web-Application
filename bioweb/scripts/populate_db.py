import os
import sys
import django
import csv
# from collections import defaultdict
from django.utils import timezone

# initialise the django system
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# tell where the settings file for our project it
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bioweb.settings')
django.setup()

# import various models we wrote, that we want to insert data into
from genedata.models import *

# get the path of the csv files
data_sequences = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'csv/assignment_data_sequences.csv')
data_set = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'csv/assignment_data_set.csv')
pfam_descriptions = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'csv/pfam_descriptions.csv')

# print(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# print(data_sequences)
# print(data_set)
# print(pfam_descriptions)

#initialise empty data structure
proteinid_sequence_ref = set()

taxonomy_set = set()
protein_set = set()
domain_set = set()
pfam_set = set()

taxonomy_protein_set = set()
taxonomy_pfam_set = set()

# use to check time taken for the csv data to be inserted into the database
start_time = timezone.now()

# open the data_sequnces file that contains protein_id and sequence
with open(data_sequences) as csv_file:
    # pass file to csv reader that splits each line up with the comma delimeter,
    # and passes back a python list
    data = csv.reader(csv_file, delimiter=',')

    # iterate through the rows, each time return a python list
    for row in data:
        # protein_id, sequence [adding data to the set]
        proteinid_sequence_ref.add((row[0], row[1]))

        # print(', '.join(row))



# open the data_set file that contains protein_id and sequence
with open(data_set) as csv_file:
    # pass file to csv reader that splits each line up with the comma delimeter,
    # and passes back a python list
    data = csv.reader(csv_file, delimiter=',')

    # iterate through the rows, each time return a python list
    for row in data:
        # index 3 in data_set csv file contains genus and species data, which is seperated by a ' '
        # so I have to split them and store them individually
        genus_species_pairs = row[3].split(' ')

        # loop through the whole list of genus_species_pairs
        for index in range(len(genus_species_pairs)):
            # save index 0 as genus
            genus = genus_species_pairs[0]

            # there are some data that has more than one ' ', which results in the index to be more than 1
            # to ensure that the species data is saved correctly, I wrote an if statement to 
            # check that if the index is more than 1,
            if index > 1:
                # the remaining 'index' of species data will still be parsed into the species variable
                species = genus_species_pairs[1]+ " " + genus_species_pairs[index]
            else:
                # else, I can just parse the data into species variable normally as per genus above
                species = genus_species_pairs[1]
        # print(genus + ", " + species)

        # taxa_id, clade, genus, species [adding data to the set]
        taxonomy_set.add((row[1], row[2], genus, species))

        # print(taxonomy_set)
        
        # this set contains protein_id and sequence from data_sequences.csv,
        # which we will use to parse into the protein table model
        for entry in proteinid_sequence_ref:
            if row[0] == entry[0]:
                # protein_id, sequence, length, taxonomy[fk]
                protein_set.add((entry[0], entry[1], row[8], row[1]))

                # pfam_id, description, start, stop, protein_id[fk]
                # pfam_id is a foreign key referenced from pfam model, so I am parsing in the domain_id in data_set.csv
                # protein_id is a foreign key referenced from protein model, so I am parsing it in from the proteinid_sequence_ref set
                # same goes for protein_id
                domain_set.add((row[5], row[4], row[6], row[7], entry[0]))

                # taxa_id[fk], protein_id[fk] [link table]
                # protein_id is a foreign key referenced from protein model, so I am parsing it in from the proteinid_sequence_ref set
                taxonomy_protein_set.add((row[1], entry[0]))

        # taxa_id[fk], pfam_id[fk] [link table]
        # pfam_id is a foreign key referenced from pfam model, so I am parsing in the domain_id in data_set.csv
        taxonomy_pfam_set.add((row[1], row[5]))



# open the pfam_descriptions file that contains protein_id and sequence
with open(pfam_descriptions) as csv_file:
    # pass file to csv reader that splits each line up with the comma delimeter,
    # and passes back a python list
    data = csv.reader(csv_file, delimiter=',')

    # iterate through the rows, each time return a python list
    for row in data:
        # domain_id, domain_description [adding data to the set]
        pfam_set.add((row[0], row[1]))

        # print(', '.join(row))



# clear out the underlying database to make sure there is no residual data 
# or previous data from any attempt to save for each table in turn against delete all objects
Taxonomy_Pfam.objects.all().delete()
Taxonomy_Protein.objects.all().delete()
Domains.objects.all().delete()
Protein.objects.all().delete()
Pfam.objects.all().delete()
Taxonomy.objects.all().delete()


#----------------------------takes around 25 seconds----------------------------#
 # keep track of which row is used to reference the foreign keys
taxonomy_rows = {}
protein_rows = {}
pfam_rows = {}

# lists for appending objects to it, used for bulk_create
taxonomy_list = []
protein_list = []
pfam_list = []
domain_list = []
taxonomy_protein_list = []
taxonomy_pfam_list = []

# each entry in taxonomy_set data structure
for entry in taxonomy_set:
    # initialise Taxonomy object in to a variable
    obj = Taxonomy(taxa_id = entry[0], clade = entry[1], genus = entry[2], species = entry[3])
    # append Pfam object into list
    taxonomy_list.append(obj)
    # keep track of pfam_rows, keep a copy of it, need to use these values as foreign keys
    taxonomy_rows[entry[0]] = obj
# use bulk_create and create the pfam rows from the list, bulk_create lessens the time taken
Taxonomy.objects.bulk_create(taxonomy_list)



# each entry in protein_set data structure
for entry in protein_set:
    # initialise Protein object in to a variable
    obj = Protein(protein_id = entry[0], sequence = entry[1], length = entry[2], taxonomy = taxonomy_rows[entry[3]])
    # append Pfam object into list
    protein_list.append(obj)
    # keep track of pfam_rows, keep a copy of it, need to use these values as foreign keys
    protein_rows[entry[0]] = obj
# use bulk_create and create the pfam rows from the list, bulk_create lessens the time taken
Protein.objects.bulk_create(protein_list)



# each entry in pfam_set data structure
for entry in pfam_set:
    # initialise Pfam object in to a variable
    obj = Pfam(domain_id = entry[0], domain_description = entry[1])
    # append Pfam object into list
    pfam_list.append(obj)
    # keep track of pfam_rows, keep a copy of it, need to use these values as foreign keys
    pfam_rows[entry[0]] = obj
    # print(pfam_rows[entry[0]])
# use bulk_create and create the pfam rows from the list, bulk_create lessens the time taken
Pfam.objects.bulk_create(pfam_list)



# each entry in domain_set data structure
for entry in domain_set:
    # initialise Pfam object in to a variable
    obj = Domains(pfam_id = pfam_rows[entry[0]], description = entry[1], start = entry[2], stop = entry[3], protein_id = protein_rows[entry[4]])
    # append Domain object into list
    domain_list.append(obj)
# use bulk_create and create the domain rows from the list, bulk_create lessens the time taken
Domains.objects.bulk_create(domain_list)



# each entry in taxonomy_protein_set data structure
for entry in taxonomy_protein_set:
    # initialise Pfam object in to a variable
    obj = Taxonomy_Protein(taxa_id = Taxonomy.objects.get(taxa_id=int(entry[0])), protein_id = protein_rows[entry[1]])
    # append Taxonomy_Protein object into list
    taxonomy_protein_list.append(obj)
# use bulk_create and create the taxonomy_protein rows from the list, bulk_create lessens the time taken
Taxonomy_Protein.objects.bulk_create(taxonomy_protein_list)



# each entry in taxonomy_pfam_set data structure
for entry in taxonomy_pfam_set:
    # initialise Taxonomy_Pfam object in to a variable
    obj = Taxonomy_Pfam(taxa_id = Taxonomy.objects.get(taxa_id=int(entry[0])), pfam_id = pfam_rows[entry[1]])
    # append Taxonomy_Pfam object into list
    taxonomy_pfam_list.append(obj)
# use bulk_create and create the taxonomy_pfam rows from the list, bulk_create lessens the time taken
Taxonomy_Pfam.objects.bulk_create(taxonomy_pfam_list)


end_time = timezone.now()
print(f"Loading CSV took: {(end_time-start_time).total_seconds()} seconds.")









#----------------------------Previous version of creating object and saving to database----------------------------#
#----------------------------takes around 160-170 seconds----------------------------#
#  # keep track of which row is used to reference the foreign keys
# taxonomy_rows = {}
# protein_rows = {}
# pfam_rows = {}

# # each entry in taxonomy_set data structure
# for entry in taxonomy_set:
#     # create new object row data, that has columns called taxa_id, clade, genus, species
#     row = Taxonomy.objects.create(taxa_id = entry[0], clade = entry[1], genus = entry[2], species = entry[3])
#     # save row to database, equivalent to sql insert statement
#     row.save()

#     # keep track of taxonomy_rows, keep a copy of it, need to use these values as foreign keys
#     taxonomy_rows[entry[0]] = row


# # each entry in protein_set data structure
# for entry in protein_set:
#     # create new object row data, that has columns called protein_id, taxonomy[fk], sequence, length
#     # taxonomy field is an foreign key referenced from taxanomy model table, so populate the field with taxonomy_rows[entry[1]]
#     row = Protein.objects.create(protein_id = entry[0], taxonomy = taxonomy_rows[entry[1]], sequence = entry[2], length = entry[3])
#     # save row to database, equivalent to sql insert statement
#     row.save()

#     # keep track of protein_rows, keep a copy of it, need to use these values as foreign keys
#     protein_rows[entry[0]] = row


# # each entry in pfam_set data structure
# for entry in pfam_set:
#     # create new object row data, that has columns called domain_id, domain_description
#     row = Pfam.objects.create(domain_id = entry[0], domain_description = entry[1])
#     # save row to database, equivalent to sql insert statement
#     row.save()

#     # keep track of pfam_rows, keep a copy of it, need to use these values as foreign keys
#     pfam_rows[entry[0]] = row


# # each entry in domain_set data structure
# for entry in domain_set:
#     # create new object row data, that has columns called pfam_id[fk], protein_id[fk], description, start, stop
#     row = Domains.objects.create(pfam_id = pfam_rows[entry[0]], protein_id = protein_rows[entry[1]], description = entry[2], start = entry[3], stop = entry[4])
#     # save row to database, equivalent to sql insert statement
#     row.save()



# # each entry in taxonomy_protein_set data structure
# for entry in taxonomy_protein_set:
#     # create new object row data, that has columns called taxa_id[fk], protein_id[fk]
#     # row = Taxonomy_Protein.objects.create(taxa_id_id = entry[0], protein_id = protein_rows[entry[1]])
#     row = Taxonomy_Protein.objects.create(taxa_id = Taxonomy.objects.get(taxa_id=int(entry[0])), protein_id = protein_rows[entry[1]])
#     # save row to database, equivalent to sql insert statement
#     row.save()


# # each entry in taxonomy_domain_set data structure
# for entry in taxonomy_domain_set:
#     # create new object row data, that has columns called taxa_id[fk], pfam_id[fk]
#     # row = Taxonomy_Domain.objects.create(taxa_id_id = entry[0], pfam_id = pfam_rows[entry[1]])
#     row = Taxonomy_Domain.objects.create(taxa_id = Taxonomy.objects.get(taxa_id=int(entry[0])), pfam_id = pfam_rows[entry[1]])
#     # save row to database, equivalent to sql insert statement
#     row.save()
import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

# Create your tests here.


# http://127.0.0.1:8000/api/protein/A0A016S8J7
class ProteinSerializer_Test(APITestCase):
    protein = None
    proteinserializer = None

    # setup Protein_Factory and ProteinSerializer for testing
    def setUp(self):
        self.protein = Protein_Factory.create(protein_id = self.protein)
        self.proteinserializer = ProteinSerializer(instance=self.protein)

    # reset model and factory
    def tearDown(self):
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()
        Taxonomy_Factory.reset_sequence(0)
        Protein_Factory.reset_sequence(0)

    # check if the data.keys returned matched the fields
    def test_ProteinDetailSuccess(self):
        data = self.proteinserializer.data
        self.assertEqual(set(data.keys()), set(['protein_id', 
                                                'sequence', 
                                                'length', 
                                                'taxonomy',
                                                'domains']))

    # check if the correct data is returned
    def test_ProteinSerilaiserGeneIDHasCorrectData(self):
        data = self.proteinserializer.data
        self.assertEqual(data['protein_id'], self.protein.protein_id)
        self.assertEqual(data['sequence'], self.protein.sequence)
        self.assertEqual(data['length'], self.protein.length)
        self.assertEqual(data['taxonomy']["taxa_id"], self.protein.taxonomy.taxa_id)
        self.assertEqual(data['taxonomy']["clade"], self.protein.taxonomy.clade)
        self.assertEqual(data['taxonomy']["genus"], self.protein.taxonomy.genus)
        self.assertEqual(data['taxonomy']["species"], self.protein.taxonomy.species)

        # self.assertEqual(data['protein_id'], "A0A016S8J7")
        # self.assertEqual(data['sequence'], "MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA")
        # self.assertEqual(data['length'], len(data['sequence']))
        # self.assertEqual(data['taxonomy']["taxa_id"], 53326)
        # self.assertEqual(data['taxonomy']["clade"], "E")
        # self.assertEqual(data['taxonomy']["genus"], "Ancylostoma")
        # self.assertEqual(data['taxonomy']["species"], "ceylanicum")



# http://127.0.0.1:8000/api/protein/A0A016S8J7
class Protein_Test(APITestCase):
    protein = None
    good_url = ''
    bad_url = ''

    # setup Protein_Factory, good_url and bad_url
    def setUp(self):
        self.protein = Protein_Factory.create(protein_id = "A0A016S8J7")
        self.good_url = reverse('Protein_api', kwargs={'pk': "A0A016S8J7"})
        self.bad_url = "/api/protein/1111/"

    # reset model and factory
    def tearDown(self):
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()
        Taxonomy_Factory.reset_sequence(0)
        Protein_Factory.reset_sequence(0)

    # test if good_url response.status_code returns 200
    def test_ProteinDetailSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        # check if data exist in these fields
        self.assertTrue('protein_id' in data)
        self.assertTrue('sequence' in data)
        self.assertTrue('length' in data)
        self.assertTrue('taxonomy' in data)
        self.assertTrue('taxa_id' in data['taxonomy'])
        self.assertTrue('clade' in data['taxonomy'])
        self.assertTrue('genus' in data['taxonomy'])
        self.assertTrue('species' in data['taxonomy'])

    # test if bad_url response.status_code returns 404
    def test_ProteinDetailReturnFailOnBadPk(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)
        


# http://127.0.0.1:8000/api/pfam/PF00360
class PfamSerializer_Test(APITestCase):
    pfam = None
    pfamserializer = None

    # setup Pfam_Factory and PfamSerializer with for testing
    def setUp(self):
        self.pfam = Pfam_Factory.create(domain_id = self.pfam)
        self.pfamserializer = PfamSerializer(instance=self.pfam)

    # reset model and factory
    def tearDown(self):
        Pfam.objects.all().delete()
        Pfam_Factory.reset_sequence(0)

    # check if the data.keys returned matched the fields
    def test_PfamDetailSuccess(self):
        data = self.pfamserializer.data
        self.assertEqual(set(data.keys()), set(['domain_id', 
                                                'domain_description']))

    # check if the correct data is returned
    def test_PfamSerilaiserGeneIDHasCorrectData(self):
        data = self.pfamserializer.data
        self.assertEqual(data['domain_id'], self.pfam.domain_id)
        self.assertEqual(data['domain_description'], self.pfam.domain_description)

        # self.assertEqual(data['domain_id'], "PF01650")
        # self.assertEqual(data['domain_description'], "PeptidaseC13family")



# http://127.0.0.1:8000/api/pfam/PF00360
class Pfam_Test(APITestCase):
    pfam = None
    good_url = ''
    bad_url = ''

    # setup Pfam_Factory, good_url and bad_url
    def setUp(self):
        self.pfam = Pfam_Factory.create(domain_id = "PF00360")
        self.good_url = reverse('Pfam_api', kwargs={'pk': "PF00360"})
        self.bad_url = "/api/pfam/1111/"

    # reset model and factory
    def tearDown(self):
        Pfam.objects.all().delete()
        Pfam_Factory.reset_sequence(0)

    # test if good_url response.status_code returns 200
    def test_PfamDetailSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        # check if data exist in these fields
        self.assertTrue('domain_id' in data)
        self.assertTrue('domain_description' in data)

    # test if bad_url response.status_code returns 404
    def test_PfamDetailReturnFailOnBadPk(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)



# http://127.0.0.1:8000/api/pfams/55661
class TaxonomyPfam_Test(APITestCase):
    taxonomy = None
    taxonomy_pfam = None
    good_url = ''
    bad_url = ''

    # setup Taxonomy_Pfam_Factory, good_url and bad_url
    def setUp(self):
        # self.taxonomy_pfam = Taxonomy_Pfam_Factory.create(taxa_id = "53326", pfam_id = "A0A091FY39")
        self.good_url = reverse('Taxonomy_Pfam_api', kwargs={'pk': "53326"})
        self.bad_url = "/api/pfams/ABCD/"

    # reset model and factory
    def tearDown(self):  
        Taxonomy.objects.all().delete()
        Domains.objects.all().delete()
        Taxonomy_Pfam.objects.all().delete()
        Taxonomy_Factory.reset_sequence(0)
        Domains_Factory.reset_sequence(0)
        Taxonomy_Pfam_Factory.reset_sequence(0)

    # test if good_url response.status_code returns 200
    def test_TaxnonomyPfamDetailSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        # check if data exist in these fields
        # self.assertTrue('id' in data[0])
        # self.assertTrue('pfam_id' in data[0])
        # self.assertTrue('domain_id' in data[0][1])
        # self.assertTrue('domain_description' in data[0][1])

    # test if bad_url response.status_code returns 404
    def test_TaxnonomyPfamDetailReturnFailOnBadPk(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)




# http://127.0.0.1:8000/api/proteins/55661
class TaxonomyProtein_Test(APITestCase):
    taxanomy_protein = None
    good_url = ''
    bad_url = ''

    # setup Taxonomy_Protein_Factory, good_url and bad_url
    def setUp(self):
        #self.taxanomy_protein = Taxonomy_Protein_Factory.create(taxa_id = "53326", protein_id = "A0A091FY39")
        self.good_url = reverse('Taxonomy_Protein_api', kwargs={'pk': "53326"})
        self.bad_url = "/api/proteins/ABCD/"

    def tearDown(self):  
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()
        Taxonomy_Protein.objects.all().delete()
        Taxonomy_Factory.reset_sequence(0)
        Protein_Factory.reset_sequence(0)
        Taxonomy_Protein_Factory.reset_sequence(0)

    # test if good_url response.status_code returns 200
    def test_TaxnonomyProteinDetailSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        # check if data exist in these fields
        # self.assertTrue('id' in data[0])
        # self.assertTrue('protein_id' in data[0])

    # test if bad_url response.status_code returns 404
    def test_TaxnonomyProteinDetailReturnFailOnBadPk(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)
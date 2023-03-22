from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response


# api/protein/
class Protein_Create(mixins.CreateModelMixin, generics.GenericAPIView):
    # get model table
    queryset = Protein.objects.all()
    # get serializer class
    serializer_class = CreateProteinSerializer
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



# api/protein/<str:pk>
class Protein_Detail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    # get model table
    queryset = Protein.objects.all()
    # get serializer class
    serializer_class = ProteinSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



# api/pfam/<str:pk>
class Pfam_Detail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    # get model table
    queryset = Pfam.objects.all()
    # get serializer class
    serializer_class = PfamSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



# api/proteins/<int:pk>
class Taxonomy_Protein_Detail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    # get the id[pk] and protein_id
    def get(self, request, *args, **kwargs):
        # get model table
        queryset = Taxonomy_Protein.objects.all()
        # get the pk
        pk = self.kwargs.get('pk')
        # filter the queryset to ensure that only field 'id' and 'protein_id' are returned
        result = queryset.filter(taxa_id = pk).values('id', 'protein_id')
        # return the result
        return Response(result)



# api/pfams/<int:pk>
class Taxonomy_Pfam_Detail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    # get the id[pk] and pfam_id
    def get(self, request, *args, **kwargs):
        # get model table
        queryset = Taxonomy_Pfam.objects.all()
        # get the pk
        pk = self.kwargs['pk']
        # filter the queryset to ensure that only field 'id' and 'pfam_id' are returned
        result = queryset.filter(taxa_id = pk).values('id', 'pfam_id')
        
        # for each entry in the filtered results
        for entry in result:
            # get model table
            queryset = Pfam.objects.all()
            # get the pfam_id from Pfam model
            pfam_id = entry.get('pfam_id')
            # filter the queryset to ensure that only field 'id' and 'pfam_id' are returned
            pfam_details = queryset.filter(domain_id = pfam_id).values('domain_id', 'domain_description')
            entry['pfam_id'] = pfam_details

        # return the result
        return Response(result)



# api/coverage/<str:pk>
class Coverage(mixins.RetrieveModelMixin, generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # get protein model table
        protein = Protein.objects.all()
        # get domain model table
        domain = Domains.objects.all()
        # get the pk
        pk = self.kwargs.get('pk')
        # filter the queryset to ensure that only field 'length' is returned
        protein_result = protein.filter(protein_id = pk).values('length')
        # filter the queryset to ensure that only field 'start' and 'stop' are returned
        domain_result = domain.filter(protein_id = pk).values('start', 'stop')

        lengthSum = 0
        startSum = 0
        stopSum = 0

        for entry in protein_result:
            length = entry.get('length')
            lengthSum = lengthSum + length

        for entry in domain_result:
            start = entry.get('start')
            startSum = startSum + start
            stop = entry.get('stop')
            stopSum = stopSum + stop
        coverage = str(abs((startSum - stopSum)/length))

        return Response("coverage:  " + coverage)
            
        

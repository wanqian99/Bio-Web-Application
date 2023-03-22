from django.urls import include, path
from . import views
from . import api

urlpatterns = [
    # POST http://127.0.0.1:8000/api/protein/ - add a new record
    path('api/protein/', api.Protein_Create.as_view(), name='Create_Protein_api'),

    # GET  http://127.0.0.1:8000/api/protein/[PROTEIN ID] - return the protein sequence and all we know about it
    path('api/protein/<str:pk>', api.Protein_Detail.as_view(), name='Protein_api'),

    # GET  http://127.0.0.1:8000/api/pfam/[PFAM ID] - return the domain and it's description
    path('api/pfam/<str:pk>', api.Pfam_Detail.as_view(), name='Pfam_api'),

    # GET  http://127.0.0.1:8000/api/proteins/[TAXA ID] - return a list of all proteins for a given organism
    path('api/proteins/<int:pk>', api.Taxonomy_Protein_Detail.as_view(), name='Taxonomy_Protein_api'),

    # GET  http://127.0.0.1:8000/api/pfams/[TAXA ID] - return a list of all domains in all the proteins for a given organism.
    path('api/pfams/<int:pk>', api.Taxonomy_Pfam_Detail.as_view(), name='Taxonomy_Pfam_api'),

    # GET  http://127.0.0.1:8000/api/coverage/[PROTEIN ID] - return the domain coverage for a given protein. 
    # That is Sum of the protein domain lengths (start-stop)/length of protein.
    path('api/coverage/<str:pk>', api.Coverage.as_view(), name='Coverage_api'),
]
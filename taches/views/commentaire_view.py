#from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from taches.models.commentaire_model import Commentaire
from taches.serializers.commentaire_serializer import CommentaireSerializer



class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.select_related("tache", "user")
    serializer_class = CommentaireSerializer

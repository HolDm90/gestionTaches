#from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from taches.models.statut_model import Statut
from taches.serializers.statut_serializer import StatutSerializer



class StatutViewSet(viewsets.ModelViewSet):
    queryset = Statut.objects.all()
    serializer_class = StatutSerializer
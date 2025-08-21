#from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from taches.models.priorite_model import Priorite
from taches.serializers.priorite_serializer import PrioriteSerializer


class PrioriteViewSet(viewsets.ModelViewSet):
    queryset = Priorite.objects.all()
    serializer_class = PrioriteSerializer
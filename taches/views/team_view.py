#from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from taches.models.team_model import Team
from taches.serializers.team_serializer import TeamSerializer




class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.prefetch_related("taches", "teammembers_set")
    serializer_class = TeamSerializer
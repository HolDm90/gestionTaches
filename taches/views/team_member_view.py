#from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from taches.models.team_member_model import TeamMembers
from taches.serializers.team_member_serializer import TeamMembersSerializer


class TeamMembersViewSet(viewsets.ModelViewSet):
    queryset = TeamMembers.objects.select_related("team", "user")
    serializer_class = TeamMembersSerializer
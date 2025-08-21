#from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from taches.models.user_model import User
from taches.serializers.user_serializer import UserSerializer



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
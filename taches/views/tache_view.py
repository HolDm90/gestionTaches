#from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from taches.models.tache_model import Tache
from taches.serializers.tache_serializer import TacheSerializer



class TacheViewSet(viewsets.ModelViewSet):
    queryset = Tache.objects.select_related("equipe", "statut", "priorite")
    serializer_class = TacheSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            taches = [Tache(**item) for item in serializer.validated_data]
            Tache.objects.bulk_create(taches)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return super().create(request, *args, **kwargs)
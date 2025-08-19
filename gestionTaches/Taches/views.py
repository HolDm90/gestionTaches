#from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from  Taches.serializers import (UserSerializer, TeamSerializer, StatutSerializer, 
PrioriteSerializer, TacheSerializer, TeamMembersSerializer, CommentaireSerializer)
from .models import *




class TacheViewSet(viewsets.ViewSet):
     

      # GET /taches/
    def list(self, request):
        taches = Tache.objects.all()
        serializer = TacheSerializer(taches, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)

       # GET /taches/{id}/
    def retrieve(self, request, pk=None):
        tache = get_object_or_404(queryset, pk=pk)
        serializer = TacheSerializer(tache)
        return Response(serializer.data,  status=status.HTTP_200_OK)


       #P POST /tache
    def create(self, request):
        serializer = TacheSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        # PUT /taches/{id}/
    def update(self, request, pk=None):
        taache = get_object_or_404(queryset, pk=pk)
        serializer = TacheSerializer(tache, data=request.data)
        if serializer.is_valid():
            seralizer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



     # PATCH /taches/{id}/
    def partial_update(self, request, pk=None):
        tache = get_object_or_404(Tache, pk=pk)
        serializer = TacheSerializer(tache, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




     # DELETE /taches/{id}/
    def destroy(self, request, pk=None):
        tache = get_object_or_404(Tache, pk=pk)
        tache.delete()
        return Response({"message": "Tâche supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)         
    


class  TeamViewSet(viewsets.ViewSet):


        # GET /team/
    def list(self, request):
        teams = Tache.objects.all()
        serializer = TacheSerializer(teams, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)



         # GET /team/{id}/
    def retrieve(self, request, pk=None):
        team = get_object_or_404(queryset, pk=pk)
        serializer = TacheSerializer(tache)
        return Response(serializer.data,  status=status.HTTP_200_OK)
    


          #P POST /taem
    def create(self, request):
        serializer = TacheSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




       # PUT /taem/{id}/
    def update(self, request, pk=None):
        taache = get_object_or_404(queryset, pk=pk)
        serializer = TacheSerializer(tache, data=request.data)
        if serializer.is_valid():
            seralizer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.prefetch_related("taches", "teammembers_set")
    serializer_class = TeamSerializer


class StatutViewSet(viewsets.ModelViewSet):
    queryset = Statut.objects.all()
    serializer_class = StatutSerializer


class PrioriteViewSet(viewsets.ModelViewSet):
    queryset = Priorite.objects.all()
    serializer_class = PrioriteSerializer


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


class TeamMembersViewSet(viewsets.ModelViewSet):
    queryset = TeamMembers.objects.select_related("team", "user")
    serializer_class = TeamMembersSerializer


class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.select_related("tache", "user")
    serializer_class = CommentaireSerializer

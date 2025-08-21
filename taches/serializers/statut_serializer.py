from taches.models import User, Team, TeamMembers, Statut, Priorite, Tache, Commentaire
from rest_framework import serializers


     
class StatutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statut
        fields = ["id", "label"]
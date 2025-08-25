from rest_framework import serializers
from taches.models.tache_model import Tache

   

class TacheSerializer(serializers.ModelSerializer):
    equipe = serializers.StringRelatedField()
    statut = serializers.StringRelatedField()
    priorite = serializers.StringRelatedField()

    class Meta:
        model = Tache
        fields = "__all__"
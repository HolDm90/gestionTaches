from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_validated"]



class TeamSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"

     
class StatutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statut
        fields = ["id", "label"]



class PrioriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Priorite
        fields = ["id", "label"]




class TacheSerializer(serializers.ModelSerializer):
    equipe = serializers.StringRelatedField()
    statut = serializers.StringRelatedField()
    priorite = serializers.StringRelatedField()

    class Meta:
        model = Tache
        fields = "__all__"




class TeamMembersSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    team = serializers.StringRelatedField()

    class Meta:
        model = TeamMembers
        fields = "__all__"


class CommentaireSerializer(serializers.ModelSerializer):
    auteur = serializers.StringRelatedField()
    reponses = serializers.SerializerMethodField()

    class Meta:
        model = Commentaire
        fields = "__all__"

    def get_reponses(self, obj):
        return CommentaireSerializer(obj.reponses.all(), many=True).data

# taches/serializers/team_serializer.py
from rest_framework import serializers
from taches.models.team_model import Team
from taches.models.team_member_model import TeamMembers
from taches.serializers.user_serializer import UserSerializer

class TeamSerializer(serializers.ModelSerializer):
    # Liste complète des membres de l'équipe
    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ["id", "nom", "members"]

    def get_members(self, obj):
        # On récupère tous les membres validés de l'équipe
        team_members = TeamMembers.objects.filter(team=obj).select_related("user")
        return UserSerializer([tm.user for tm in team_members], many=True).data

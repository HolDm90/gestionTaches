from rest_framework import serializers
from taches.models.team_member_model import TeamMembers
from taches.serializers.user_serializer import UserSerializer
from taches.serializers.team_serializer import TeamSerializer

class TeamMembersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = TeamMembers
        fields = ["id", "team", "user", "date_joined"]

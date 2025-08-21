from rest_framework import serializers
from taches.models.team_model import Team
from taches.serializers.user_serializer import UserSerializer

class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"

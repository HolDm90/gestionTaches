from rest_framework import serializers
from taches.models.team_member_model import TeamMembers

class TeamMembersSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    team = serializers.StringRelatedField()

    class Meta:
        model = TeamMembers
        fields = "__all__"
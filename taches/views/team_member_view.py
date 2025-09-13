# taches/views/team_member_view.py
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from taches.models.team_member_model import TeamMembers
from taches.serializers.team_member_serializer import TeamMembersSerializer
from taches.permissions import IsValidatedUser

@extend_schema(tags=["Membres d’équipe"])
class TeamMembersViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lecture seule des membres d'équipe.
    - Admin : voir tous les membres
    - Chef : voir ses équipes
    - Membre : voir sa participation uniquement
    """
    queryset = TeamMembers.objects.all()
    serializer_class = TeamMembersSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return TeamMembers.objects.select_related("team", "user").all()

        elif user.has_group("Chef d’équipe"):
            # Chef : voir les membres de ses équipes
            return TeamMembers.objects.filter(
                team__teammembers__user=user
            ).select_related("team", "user").distinct()

        elif user.has_group("Membre"):
            # Membre : voir seulement ses propres participations
            return TeamMembers.objects.filter(user=user).select_related("team", "user").distinct()

        return TeamMembers.objects.none()

# taches/views/team_view.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from taches.models.team_model import Team
from taches.models.team_member_model import TeamMembers
from taches.serializers.team_serializer import TeamSerializer
from taches.permissions import IsChefEquipe, IsValidatedUser


@extend_schema(tags=["Équipes"])
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_permissions(self):
        """
        Gestion des permissions selon l’action :
        - Seuls les chefs peuvent créer/modifier/supprimer.
        - Tous les utilisateurs validés peuvent lire.
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsChefEquipe]
        else:
            permission_classes = [IsValidatedUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Définition de la visibilité des équipes selon le rôle :
        - Chef : ses propres équipes
        - Membre : ses propres équipes
        - Admin : toutes les équipes
        """
        user = self.request.user

        if user.is_superuser:
            return Team.objects.all()

        elif user.has_group("Chef d’équipe"):
            return Team.objects.filter(teammembers__user=user).distinct()

        elif user.has_group("Membre"):
            return Team.objects.filter(teammembers__user=user).distinct()

        return Team.objects.none()

    def create(self, request, *args, **kwargs):
        """
        Seul un chef peut créer une équipe.
        Lors de la création, il est automatiquement ajouté comme membre (chef).
        """
        if not request.user.has_group("Chef d’équipe"):
            return Response(
                {"error": "Seuls les chefs d’équipe peuvent créer une équipe."},
                status=status.HTTP_403_FORBIDDEN
            )

        response = super().create(request, *args, **kwargs)

        # Ajouter automatiquement le créateur comme membre de l’équipe
        TeamMembers.objects.get_or_create(
            team_id=response.data["id"],
            user=request.user
        )

        return response

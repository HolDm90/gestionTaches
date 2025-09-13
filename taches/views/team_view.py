# taches/views/team_view.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from django.contrib.auth import get_user_model
from taches.models.team_model import Team
from taches.models.team_member_model import TeamMembers
from taches.serializers.team_serializer import TeamSerializer
from taches.serializers.add_member_serializer import AddMemberSerializer
from taches.permissions import IsChefEquipe, IsValidatedUser

User = get_user_model()

@extend_schema(tags=["Équipes"])
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "add_member", "remove_member"]:
            permission_classes = [IsChefEquipe]
        else:
            permission_classes = [IsValidatedUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Team.objects.all()
        elif user.has_group("Chef d’équipe") or user.has_group("Membre"):
            return Team.objects.filter(teammembers__user=user).distinct()
        return Team.objects.none()

    def create(self, request, *args, **kwargs):
        if not request.user.has_group("Chef d’équipe"):
            return Response(
                {"error": "Seuls les chefs d’équipe peuvent créer une équipe."},
                status=status.HTTP_403_FORBIDDEN
            )

        response = super().create(request, *args, **kwargs)

        # Ajoute automatiquement le créateur comme membre (chef)
        TeamMembers.objects.get_or_create(
            team_id=response.data["id"],
            user=request.user
        )
        return response

    # ----------------------------------
    # Gestion des membres par le chef
    # ----------------------------------

    @extend_schema(request=AddMemberSerializer, responses={201: TeamSerializer})
    @action(detail=True, methods=["post"], url_path="add-member")
    def add_member(self, request, pk=None):
        team = self.get_object()
        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]
        member = User.objects.filter(id=user_id, groups__name="Membre", is_validated=True).first()
        if not member:
            return Response({"error": "Utilisateur non valide ou non membre."}, status=status.HTTP_400_BAD_REQUEST)

        team_member, created = TeamMembers.objects.get_or_create(team=team, user=member)
        return Response(TeamSerializer(team).data, status=status.HTTP_201_CREATED)

    @extend_schema(request=AddMemberSerializer, responses={204: None})
    @action(detail=True, methods=["post"], url_path="remove-member")
    def remove_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get("user_id")
        deleted, _ = TeamMembers.objects.filter(team=team, user_id=user_id).delete()

        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Aucun membre trouvé avec cet ID dans l’équipe."}, status=status.HTTP_400_BAD_REQUEST)

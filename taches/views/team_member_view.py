# taches/views/team_member_view.py
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from django.contrib.auth import get_user_model
from taches.models.team_member_model import TeamMembers
from taches.serializers.team_member_serializer import TeamMembersSerializer
from taches.permissions import IsChefEquipe, IsValidatedUser

User = get_user_model()


class AddMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


@extend_schema(tags=["Membres d’équipe"])
class TeamMembersViewSet(viewsets.ModelViewSet):
    queryset = TeamMembers.objects.all()
    serializer_class = TeamMembersSerializer

    def get_permissions(self):
        """
        - Gestion (ajout/suppression) → réservé aux chefs d’équipe
        - Lecture → ouverte à tout utilisateur validé
        """
        if self.action in ["create", "update", "partial_update", "destroy", "add_member", "remove_member"]:
            permission_classes = [IsChefEquipe]
        else:
            permission_classes = [IsValidatedUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            # Admin : accès lecture seule à tout
            return TeamMembers.objects.select_related("team", "user").all()

        elif user.has_group("Chef d’équipe"):
            # Chef : accès aux membres de ses équipes
            return TeamMembers.objects.filter(
                team__teammembers__user=user
            ).select_related("team", "user").distinct()

        elif user.has_group("Membre"):
            # Membre : accès seulement à ses propres participations
            return TeamMembers.objects.filter(
                user=user
            ).select_related("team", "user").distinct()

        return TeamMembers.objects.none()

    @extend_schema(
        request=AddMemberSerializer,
        responses={201: TeamMembersSerializer}
    )
    @action(detail=True, methods=["post"], url_path="add-member")
    def add_member(self, request, pk=None):
        """
        Ajouter un membre à une équipe.
        Uniquement accessible au chef de l’équipe.
        """
        team_member = self.get_object()
        team = team_member.team

        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member_id = serializer.validated_data["user_id"]
        member = User.objects.filter(
            id=member_id,
            groups__name="Membre",
            is_validated=True
        ).first()

        if not member:
            return Response(
                {"error": "Utilisateur non valide ou non membre."},
                status=status.HTTP_400_BAD_REQUEST
            )

        team_member, created = TeamMembers.objects.get_or_create(
            team=team,
            user=member
        )
        return Response(TeamMembersSerializer(team_member).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=AddMemberSerializer,
        responses={204: None}
    )
    @action(detail=True, methods=["post"], url_path="remove-member")
    def remove_member(self, request, pk=None):
        """
        Supprimer un membre d’une équipe.
        Uniquement accessible au chef de l’équipe.
        """
        team_member = self.get_object()
        team = team_member.team
        user_id = request.data.get("user_id")

        deleted, _ = TeamMembers.objects.filter(team=team, user_id=user_id).delete()
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Aucun membre trouvé avec cet ID dans l’équipe."},
            status=status.HTTP_400_BAD_REQUEST
        )

# taches/views/change_password_view.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from drf_spectacular.utils import extend_schema

from taches.serializers.change_password_serializer import ChangePasswordSerializer

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: {"type": "object", "example": {"detail": "Mot de passe changé avec succès"}}},
        description="Changer son mot de passe (ancien + nouveau requis)"
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        # Vérifie l'ancien mot de passe
        if not user.check_password(old_password):
            return Response({"detail": "Ancien mot de passe incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Met à jour le mot de passe
        user.set_password(new_password)
        user.save()

        # Maintient la session active après changement
        update_session_auth_hash(request, user)

        return Response({"detail": "Mot de passe changé avec succès"}, status=status.HTTP_200_OK)

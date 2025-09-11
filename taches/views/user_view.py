# taches/views/user_view.py
from rest_framework import viewsets,  generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group
from taches.models.user_model import User
from taches.serializers.user_serializer import UserSerializer
from taches.serializers.login_serializer import CustomTokenObtainPairSerializer
from taches.permissions import IsValidatedUser, IsMembre, IsChefEquipe


from drf_spectacular.utils import extend_schema, OpenApiTypes

# ----------------------------
# CRUD admin pour gestion des utilisateurs
# ----------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related("groups")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        """
        Permet à l'admin de valider l'utilisateur et de définir son groupe.
        """
        user = serializer.save()
        group_name = self.request.data.get("group", None)
        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                user.groups.set([group])
                user.is_validated = True
                user.save()
            except Group.DoesNotExist:
                pass  # si le groupe n'existe pas, on ne fait rien

# ----------------------------
# Inscription utilisateur libre
# ----------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserSerializer,
        responses=UserSerializer,
        description="Créer un nouvel utilisateur (is_validated=False par défaut, groupe Pending)"
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_validated=False)

        # Assigner automatiquement le groupe "Pending"
        pending_group, _ = Group.objects.get_or_create(name="Pending")
        user.groups.add(pending_group)

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

# ----------------------------
# Login JWT sécurisé
# ----------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ----------------------------
# Logout (blacklist)
# ----------------------------
class LogoutView(APIView):
    permission_classes = [IsValidatedUser]

    @extend_schema(
        request={"refresh": OpenApiTypes.STR},
        responses={
            205: OpenApiTypes.STR,
            400: OpenApiTypes.STR
        },
        description="Blackliste le refresh token pour déconnecter l'utilisateur"
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Déconnexion réussie"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





# ----------------------------
# Me
# ----------------------------

class MeView(generics.RetrieveUpdateAPIView):
    """
    Endpoint pour consulter et modifier son propre profil.
    - GET : voir ses infos
    - PATCH : modifier prénom et nom
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        request=UserSerializer,
        responses=UserSerializer,
        description="Récupérer ou mettre à jour son propre profil (prenom et nom uniquement)."
    )
    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data.copy()

        # On bloque les champs sensibles
        data.pop("is_validated", None)
        data.pop("groups", None)
        data.pop("is_active", None)
        data.pop("password", None)  # on ignore le password ici

        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
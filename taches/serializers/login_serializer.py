# taches/serializers/login_serializer.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from taches.models.user_model import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        Personnalisation du contenu du JWT.
        Tout ce qui est mis ici sera encodé dans le token (access/refresh).
        """
        token = super().get_token(user)
        token['role'] = user.role
        token['is_validated'] = user.is_validated
        token['email'] = user.email
        token['username'] = user.username
        return token

    def validate(self, attrs):
        """
        Personnalisation de la réponse du login.
        """
        data = super().validate(attrs)

        # Vérifie si le compte est validé par l'admin
        if not self.user.is_validated:
            raise serializers.ValidationError(
                "Votre compte n’a pas encore été validé par un administrateur."
            )

        # Ajouter des infos dans la réponse JSON du login
        data.update({
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "role": self.user.role,
            "is_validated": self.user.is_validated,
        })
        return data

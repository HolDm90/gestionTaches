# taches/serializers/login_serializer.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from taches.models.user_model import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: User):
        """
        Personnalisation du contenu du JWT.
        Encodage des groupes au lieu de 'role'.
        """
        token = super().get_token(user)

        # On encode les groupes dans le token
        token['groups'] = [g.name for g in user.groups.all()]
        token['is_validated'] = user.is_validated
        token['email'] = user.email
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

        # Ajouter les informations de l'utilisateur dans la réponse JSON
        data.update({
            "id": self.user.id,
            "email": self.user.email,
            "is_validated": self.user.is_validated,
            "groups": [g.name for g in self.user.groups.all()],  # remplace role
        })
        return data

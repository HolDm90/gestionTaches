# taches/serializers/login_serializer.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from taches.models.user_model import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD  # généralement 'username'

    def validate(self, attrs):
        data = super().validate(attrs)

        # Vérification que l'utilisateur est validé
        if not self.user.is_validated:
            raise serializers.ValidationError("Votre compte n'a pas encore été validé par l'administrateur.")

        # Infos supplémentaires à renvoyer
        data.update({
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role
        })
        return data

from rest_framework import serializers
from taches.models.user_model import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_validated"]
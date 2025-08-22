# taches/serializers/user_serializer.py
from rest_framework import serializers
from taches.models.user_model import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'is_validated']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', None),
            is_validated=validated_data.get('is_validated', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

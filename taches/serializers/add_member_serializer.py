# taches/serializers/add_member_serializer.py
from rest_framework import serializers

class AddMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

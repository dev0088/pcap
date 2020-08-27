from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from django.contrib.auth.models import User

# class UserProfileRequestSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     username = serializers.CharField(max_length=150)
#     # password = serializers.CharField(max_length=128)
#     first_name = serializers.CharField(max_length=150)
#     last_name = serializers.CharField(max_length=150)
#     email = serializers.CharField(max_length=254)

class UserProfileRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'last_login',
        )
        read_only_fields = (
            "id",
        )
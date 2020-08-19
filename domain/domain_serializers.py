from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from .models import Domain

class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Domain
        fields = (
            'id',
            'name',
            'description',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            "id",
        )

class DomainCsvSerializer(serializers.ModelSerializer):

    class Meta:
        model = Domain
        fields = (
            'name',
            'description',
        )

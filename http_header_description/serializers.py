from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from .models import HttpHeaderDescription

class HttpHeaderDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = HttpHeaderDescription
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

class HttpHeaderDescriptionSerializerCsvSerializer(serializers.ModelSerializer):

    class Meta:
        model = HttpHeaderDescriptionSerializer
        fields = (
            'name',
            'description',
        )

from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from .models import HttpHeaderValueDescription

class HttpHeaderValueDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = HttpHeaderValueDescription
        fields = (
            'id',
            'name',
            'value',
            'description',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            "id",
        )

class HttpHeaderValueDescriptionSerializerCsvSerializer(serializers.ModelSerializer):

    class Meta:
        model = HttpHeaderValueDescription
        fields = (
            'name',
            'value',
            'description',
        )

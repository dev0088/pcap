from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from datetime import datetime
from pytz import timezone
from drf_yasg.utils import swagger_auto_schema
from .user_serializers import UserLoginSerializer, UserLoginRequestSerializer

class CustomAuthToken(ObtainAuthToken):
    # permission_classes = (AllowAny,)
    # serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        # simply delete the token to force a login
        user = request.user
        try:
            user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        
        return Response(status=status.HTTP_200_OK)
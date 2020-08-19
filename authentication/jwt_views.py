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
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from datetime import datetime
from pytz import timezone

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }

class LoginView(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        # by default attempts username / passsword combination
        response = super(LoginView, self).post(request, *args, **kwargs)
        # below will return null, but not an error, if not found :)
        res = response.data
        token = res.get('token')
        
        # token ok, get user
        if token:
            user = jwt_decode_handler(token)  # aleady json - don't serialize
        else:
            req = request.data  # try and find email in request
            email = req.get('email')
            password = req.get('password')
            username = req.get('username')

            if email is None or password is None:
                return Response(
                    {
                        'success': False, 
                        'message': 'Missing or incorrect credentials',
                        'data': req
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # email exists in request, try to find user
            try:
                user = User.objects.get(email=email)
            except:
                return Response(
                    {
                        'success': False, 
                        'message': 'User not found',
                        'data': req
                    },
                        status=status.HTTP_404_NOT_FOUND
                    )

            if not user.check_password(password):
                return Response(
                    {
                        'success': False, 
                        'message': 'Incorrect password',
                        'data': req
                    },
                    status=status.HTTP_403_FORBIDDEN
                )


            # make token from user found by email
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user = UserSerializer(user).data

        return Response(
            {
                'success': True,
                'message': 'Successfully logged in',
                'token': token,
                'user': user
            },
            status=status.HTTP_200_OK
        )

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        # simply delete the token to force a login
        user = request.user
        try:
            user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        
        return Response(status=status.HTTP_200_OK)
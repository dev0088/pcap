from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import UpdateAPIView
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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .user_profile_serializers import UserProfileRequestSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserProfileRequestSerializer(user).data(user, context={'request': request}).data
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

            if username is None or password is None:
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

        # Get user record from token user.
        user_record = User.objects.get(id=user['user_id'])
        user_data = UserProfileRequestSerializer(user_record).data
        return Response(
            {
                'success': True,
                'message': 'Successfully logged in',
                'token': token,
                'user': user_data
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

class ProfileDetail(APIView):
  id_path_param = openapi.Parameter(
          'id',
          openapi.IN_PATH,
          description="User ID",
          type=openapi.TYPE_INTEGER
  )
  
  def get_object(self, pk):
    try:
      return User.objects.get(pk=pk)
    except User.DoesNotExist:
      raise Http404


  @swagger_auto_schema(
    request_body=None,
    responses={200: UserProfileRequestSerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    """
    Get a domain info
    """
    item = self.get_object(pk)
    serializer = UserProfileRequestSerializer(item)
    return Response(serializer.data)

  @swagger_auto_schema(
    # manual_parameters=[id_path_param],
    request_body=UserProfileRequestSerializer,
    responses={200: UserProfileRequestSerializer(many=False)}
  )
  def put(self, request, pk, format=None):
    """
    Update info of a user
    """
    item = self.get_object(pk)
    data = request.data
    serializer = UserProfileRequestSerializer(item, data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response(serializer.data)

class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    # model = User
    # permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        # responses={200: ChangePasswordSerializer(many=False)}
    )
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
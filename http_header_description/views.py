import json
import requests
import time
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions, authentication
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import HttpHeaderDescription
from .serializers import HttpHeaderDescriptionSerializer

class HttpHeaderDescriptionList(APIView):
  """
  Get all http header descriptions
  """
  def get(self, request, format=None):
    items = HttpHeaderDescription.objects.all()
    serializer = HttpHeaderDescriptionSerializer(items, many=True)
    return Response(serializer.data)

class HttpHeaderDescriptionCreate(APIView):  
  @swagger_auto_schema(
    request_body=HttpHeaderDescriptionSerializer,
    responses={200: HttpHeaderDescriptionSerializer(many=False)}
  )
  def post(self, request, format=None):
    """
    Create a new http header description
    """
    serializer = HttpHeaderDescriptionSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class HttpHeaderDescriptionDetail(APIView):
  id_path_param = openapi.Parameter(
          'id',
          openapi.IN_PATH,
          description="HttpHeaderDescription ID",
          type=openapi.TYPE_INTEGER
  )
  
  def get_object(self, pk):
    try:
      return HttpHeaderDescription.objects.get(pk=pk)
    except HttpHeaderDescription.DoesNotExist:
      raise Http404


  @swagger_auto_schema(
    request_body=None,
    responses={200: HttpHeaderDescriptionSerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    """
    Get a http header description
    """
    item = self.get_object(pk)
    serializer = HttpHeaderDescriptionSerializer(item)
    return Response(serializer.data)

  @swagger_auto_schema(
    # manual_parameters=[id_path_param],
    request_body=HttpHeaderDescriptionSerializer,
    responses={200: HttpHeaderDescriptionSerializer(many=False)}
  )
  def put(self, request, pk, format=None):
    """
    Update info of a http header description
    """
    item = self.get_object(pk)
    data = request.data
    serializer = HttpHeaderDescriptionSerializer(item, data=data)
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

  @swagger_auto_schema(
    request_body=None,
  )
  def delete(self, request, pk, format=None):
    """
    Delete a http header description
    """
    item = self.get_object(pk)
    item.delete()
    return Response({'id': int(pk)}, status=status.HTTP_200_OK)
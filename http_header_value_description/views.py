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
from .models import HttpHeaderValueDescription
from .serializers import HttpHeaderValueDescriptionSerializer

class HttpHeaderValueDescriptionList(APIView):
  """
  Get all http header value descriptions
  """
  def get(self, request, format=None):
    items = HttpHeaderValueDescription.objects.all()
    serializer = HttpHeaderValueDescriptionSerializer(items, many=True)
    return Response(serializer.data)

class HttpHeaderValueDescriptionCreate(APIView):  
  @swagger_auto_schema(
    request_body=HttpHeaderValueDescriptionSerializer,
    responses={200: HttpHeaderValueDescriptionSerializer(many=False)}
  )
  def post(self, request, format=None):
    """
    Create a new http header value description
    """
    serializer = HttpHeaderValueDescriptionSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class HttpHeaderValueDescriptionDetail(APIView):
  id_path_param = openapi.Parameter(
          'id',
          openapi.IN_PATH,
          description="HttpHeaderValueDescription ID",
          type=openapi.TYPE_INTEGER
  )
  
  def get_object(self, pk):
    try:
      return HttpHeaderValueDescription.objects.get(pk=pk)
    except HttpHeaderValueDescription.DoesNotExist:
      raise Http404


  @swagger_auto_schema(
    request_body=None,
    responses={200: HttpHeaderValueDescriptionSerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    """
    Get a http header value description
    """
    item = self.get_object(pk)
    serializer = HttpHeaderValueDescriptionSerializer(item)
    return Response(serializer.data)

  @swagger_auto_schema(
    # manual_parameters=[id_path_param],
    request_body=HttpHeaderValueDescriptionSerializer,
    responses={200: HttpHeaderValueDescriptionSerializer(many=False)}
  )
  def put(self, request, pk, format=None):
    """
    Update info of a http header value description
    """
    item = self.get_object(pk)
    data = request.data
    serializer = HttpHeaderValueDescriptionSerializer(item, data=data)
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

  @swagger_auto_schema(
    request_body=None,
  )
  def delete(self, request, pk, format=None):
    """
    Delete a http header value description
    """
    item = self.get_object(pk)
    item.delete()
    return Response({'id': int(pk)}, status=status.HTTP_200_OK)
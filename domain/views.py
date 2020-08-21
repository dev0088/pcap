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
from .models import Domain
from .domain_serializers import DomainSerializer

class DomainList(APIView):
  """
  Get all domains
  """
  def get(self, request, format=None):
    domains = Domain.objects.all()
    serializer = DomainSerializer(domains, many=True)
    return Response(serializer.data)

class DomainCreate(APIView):  
  @swagger_auto_schema(
    request_body=DomainSerializer,
    responses={200: DomainSerializer(many=False)}
  )
  def post(self, request, format=None):
    """
    Create a new domain
    """
    serializer = DomainSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class DomainDetail(APIView):
  id_path_param = openapi.Parameter(
          'id',
          openapi.IN_PATH,
          description="Domain ID",
          type=openapi.TYPE_INTEGER
  )
  
  def get_object(self, pk):
    try:
      return Domain.objects.get(pk=pk)
    except Domain.DoesNotExist:
      raise Http404


  @swagger_auto_schema(
    request_body=None,
    responses={200: DomainSerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    """
    Get a domain info
    """
    item = self.get_object(pk)
    serializer = DomainSerializer(item)
    return Response(serializer.data)

  @swagger_auto_schema(
    # manual_parameters=[id_path_param],
    request_body=DomainSerializer,
    responses={200: DomainSerializer(many=False)}
  )
  def put(self, request, pk, format=None):
    """
    Update info of a domain
    """
    item = self.get_object(pk)
    data = request.data
    serializer = DomainSerializer(item, data=data)
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

  @swagger_auto_schema(
    request_body=None,
  )
  def delete(self, request, pk, format=None):
    """
    Delete a domain
    """
    item = self.get_object(pk)
    item.delete()
    return Response({'id': int(pk)}, status=status.HTTP_200_OK)
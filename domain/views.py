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

class DomainDetail(APIView):
  
  def get_object(self, pk):
    try:
      return Domain.objects.get(pk=pk)
    except Domain.DoesNotExist:
      raise Http404

  """
  Get a doman info
  """
  @swagger_auto_schema(
    request_body=None,
    responses={200: DomainSerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = DomainSerializer(item)
    return Response(serializer.data)

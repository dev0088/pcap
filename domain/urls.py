from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from domain import views

urlpatterns = [
  url(r'^all/', views.DomainList.as_view()),
  url(r'^(?P<pk>[0-9]+)/', views.DomainDetail.as_view()),
]
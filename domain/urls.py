from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from domain import views, csv_views

urlpatterns = [
  url(r'^all/', views.DomainList.as_view()),
  url(r'^create/', views.DomainCreate.as_view()),
  url(r'^(?P<pk>[0-9]+)/', views.DomainDetail.as_view()),
  url(r'^export-csv/', csv_views.ExportCsv.as_view()),
  url(r'^import-csv/', csv_views.ImportCsv.as_view()),
]
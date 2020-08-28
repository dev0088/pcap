from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, custom_csv_views

urlpatterns = [
  url(r'^all/', views.HttpHeaderDescriptionList.as_view()),
  url(r'^create/', views.HttpHeaderDescriptionCreate.as_view()),
  url(r'^(?P<pk>[0-9]+)/', views.HttpHeaderDescriptionDetail.as_view()),
  url(r'^export-csv/', custom_csv_views.ExportCsv.as_view()),
  url(r'^import-csv/', custom_csv_views.ImportCsv.as_view()),
]
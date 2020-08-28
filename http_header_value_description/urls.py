from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, custom_csv_views

urlpatterns = [
  url(r'^all/', views.HttpHeaderValueDescriptionList.as_view()),
  url(r'^create/', views.HttpHeaderValueDescriptionCreate.as_view()),
  url(r'^(?P<pk>[0-9]+)/', views.HttpHeaderValueDescriptionDetail.as_view()),
  url(r'^export-csv/', custom_csv_views.ExportCsv.as_view()),
  url(r'^import-csv/', custom_csv_views.ImportCsv.as_view()),
]
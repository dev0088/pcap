import datetime
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import tablib
from tablib import Dataset
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from werkzeug.utils import secure_filename
from .resources import HttpHeaderDescriptionResource

def export_csv(request):
    http_header_description_resource = HttpHeaderDescriptionResource()
    dataset = http_header_description_resource.export_with_custom_delimiter()

    t = datetime.datetime.now()
    t = '{:%Y-%m-%d_%H-%M}'.format(t)
    
    response = HttpResponse(dataset, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="http_header_descriptions-{str_date}.csv"'.format(str_date=t)
    response['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response

def import_csv(request):
    if 'file' not in request.data:
        raise ParseError("Empty content")

    # Save temp file
    f = request.data['file']
    file_name = secure_filename(request.data['fileName'])
    file_id = file_name
    tmp_file_dir = 'static/upload/'
    tmp_file_path = '{tmp_file_dir}/{file_name}'.format(
            tmp_file_dir = tmp_file_dir,
            file_name = file_name
        )
    stored_path = default_storage.save(tmp_file_path, ContentFile(f.read()))
    # Read csv file from the temp file
    new_http_header_descriptions = open(stored_path).read()
    # Read dataset with custom delimiter
    dataset = tablib.import_set(
        new_http_header_descriptions,
        format='csv',
        delimiter=settings.IMPORT_EXPORT_CSV_DELIMITER,
        headers=False
    )
    
    # Check header was appeared
    first_row = dataset[0]
    if first_row and first_row[0] == 'name':
        # Remove first row
        del dataset[0]

    dataset.headers=['name', 'description']
    http_header_description_resource = HttpHeaderDescriptionResource()
    # Test import now
    result = http_header_description_resource.import_data(dataset, dry_run=True)
    # Remove temp file
    os.remove(stored_path)

    if not result.has_errors():
        # Actually import now
        http_header_description_resource.import_data(dataset, dry_run=False)
        return Response(status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_403_FORBIDDEN)

def export_json(request):
    http_header_description_resource = HttpHeaderValueDescriptionResource()
    dataset = http_header_description_resource.export()
    response = HttpResponse(dataset.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="http_header_descriptions.json"'
    return response

def export_excel(request):
    http_header_description_resource = HttpHeaderValueDescriptionResource()
    dataset = http_header_description_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="http_header_descriptions.xls"'
    return response


class ExportCsv(APIView):
    def get(self, request, format=None):
        """
        Download csv file
        """
        return export_csv(request)


class ImportCsv(APIView):
    parser_class = (MultiPartParser,)

    def post(self, request, format=None):
        """
        Upload csv file.
        """
        return import_csv(request)
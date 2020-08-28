import datetime
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from werkzeug.utils import secure_filename
from django.template import loader
from .models import HttpHeaderDescription

def export_csv(request):
    items = HttpHeaderDescription.objects.all()
    csv_data = []
    for item in items:
        row = [item.name, item.description]
        csv_data.append(row)

    t = datetime.datetime.now()
    t = '{:%Y-%m-%d_%H-%M}'.format(t)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="http_header_descriptions-{str_date}.csv"'.format(str_date=t)
    response['Access-Control-Expose-Headers'] = 'Content-Disposition'

    template = loader.get_template('http_header_description_template.txt')
    c = {'data': csv_data}
    response.write(template.render(c))

    return response


def import_csv(request):
    if 'file' not in request.data:
        raise ParseError("Empty content")

    # Save temp file
    file_data = request.data['file']
    file_name = secure_filename(request.data['fileName'])
    file_id = file_name
    tmp_file_dir = 'static/upload/'
    tmp_file_path = '{tmp_file_dir}/{file_name}'.format(
            tmp_file_dir = tmp_file_dir,
            file_name = file_name
        )
    stored_path = default_storage.save(tmp_file_path, ContentFile(file_data.read()))
    f = open(stored_path, 'r')
    # Read csv file from the temp file
    for line in f:
        line = line.lstrip().rstrip().rstrip(',')
        line = line.split(':')
        hhd = HttpHeaderDescription()
        hhd.name = line[0].replace('"', '')
        hhd.description = line[1].replace('"', '').lstrip()
        record = HttpHeaderDescription.objects.filter(name=hhd.name).first()
        if record == None:
            hhd.save()

    # Remove temp file
    os.remove(stored_path)
    return Response(status=status.HTTP_200_OK)


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
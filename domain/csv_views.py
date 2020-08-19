from django.shortcuts import render
from django.http import HttpResponse
from .resources import DomainResource
from tablib import Dataset
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
import datetime

def export_csv(request):
    domain_resource = DomainResource()
    
    dataset = domain_resource.export()
    # databset = domain_resource.export_with_custom_delimiter()
    print('===== dataset: ', dataset)
    t = datetime.datetime.now()
    t = '{:%Y-%m-%d_%H-%M}'.format(t)

    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="domains-{str_date}.csv"'.format(str_date=t)
    return response

def export_json(request):
    domain_resource = DomainResource()
    dataset = domain_resource.export()
    response = HttpResponse(dataset.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="domains.json"'
    return response

def export_excel(request):
    domain_resource = DomainResource()
    dataset = domain_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="domains.xls"'
    return response

def simple_upload(request):
    if request.method == 'POST':
        domain_resource = DomainResource()
        dataset = Dataset()
        new_domains = request.FILES['csvfile']

        imported_data = dataset.load(new_domains.read())
        result = domain_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            domain_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')


class ExportCsv(APIView):
  """
  Export csv
  """
  def get(self, request, format=None):
    return export_csv(request)
    # domains = Domain.objects.all()
    # serializer = DomainSerializer(domains, many=True)
    # return Response(serializer.data)
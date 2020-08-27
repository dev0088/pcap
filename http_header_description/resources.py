from import_export import resources, fields
from import_export.formats import base_formats
from django.conf import settings
from .models import HttpHeaderDescription

# Extension csv with custom delimiter
class ECSV(base_formats.CSV):

    def create_dataset(self, in_stream, **kwargs):
        kwargs['delimiter'] = settings.IMPORT_EXPORT_CSV_DELIMITER
        return super().create_dataset(in_stream, **kwargs)

    def export_data(self, dataset, **kwargs):
        kwargs['delimiter'] = settings.IMPORT_EXPORT_CSV_DELIMITER
        return super().export_data(dataset, **kwargs)


class HttpHeaderDescriptionResource(resources.ModelResource):
    class Meta:
        model = HttpHeaderDescription
        fields = ('name', 'description')
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('name', 'description')
    
    def export_with_custom_delimiter(self):
        dataset = self.export()
        export_data = ECSV().export_data(dataset)
        return export_data



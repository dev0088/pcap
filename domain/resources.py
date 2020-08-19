from import_export import resources, fields
from .models import Domain


class DomainResource(resources.ModelResource):
    class Meta:
        model = Domain
        fields = ('name', 'description')
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('name', 'description')
    
    def export_with_custom_delimiter(delimiter=','):
        dataset = self.resource.export(queryset=queryset)
        export_data = base_formats.CSV().export_data(
            dataset, delimiter=delimiter,
            quoting=csv.QUOTE_ALL
        )
    
    def import_with_custom_delimiter(delimiter=','):
        dataset = self.resource.export(queryset=queryset)
        export_data = base_formats.CSV().export_data(
            dataset, delimiter=delimiter,
            quoting=csv.QUOTE_ALL
        )


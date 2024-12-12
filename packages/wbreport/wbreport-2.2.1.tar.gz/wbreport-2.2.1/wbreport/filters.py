from wbcore import filters as wb_filters
from wbreport.models import Report, ReportVersion


class ReportFilterSet(wb_filters.FilterSet):
    is_active = wb_filters.BooleanFilter(default=True)

    class Meta:
        model = Report
        fields = {
            "category": ["exact"],
            "parent_report": ["exact", "isnull"],
            "permission_type": ["exact"],
            "base_color": ["exact"],
            "mailing_list": ["exact"],
        }


class ReportVersionFilterSet(wb_filters.FilterSet):
    disabled = wb_filters.BooleanFilter(method="boolean_is_disabled", default=False)

    def boolean_is_disabled(self, queryset, name, value):
        if value is True:
            return queryset.filter(disabled=True)
        if value is False:
            return queryset.filter(disabled=False)
        return queryset

    class Meta:
        model = ReportVersion
        fields = {
            "report": ["exact"],
            "version_date": ["gte", "exact", "lte"],
            "creation_date": ["gte", "exact", "lte"],
            "update_date": ["gte", "exact", "lte"],
            "is_primary": ["exact"],
        }

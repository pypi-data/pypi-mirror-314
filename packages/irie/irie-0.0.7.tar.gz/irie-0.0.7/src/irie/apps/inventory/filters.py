import django_filters
from django.forms import CheckboxInput

class AssetFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        lookup_expr="icontains", 
        field_name="calid",
        label='Search'
    )

    cesmd_not_null = django_filters.BooleanFilter(
        label='On CESMD',
        widget=CheckboxInput(),
        method='filter_cesmd_exists'
    )

    is_complete = django_filters.BooleanFilter(
        field_name='is_complete',
        label='Is Complete',
        widget=CheckboxInput()
    )
    district = django_filters.CharFilter(
        label='District',
        method='filter_district'
    )

    def filter_cesmd_exists(self, queryset, name, value):
        if value:  # Checkbox is checked
            return queryset.exclude(cesmd__isnull=True).exclude(cesmd__exact='')
        return queryset

    def filter_district(self, queryset, name, value):
        return [
            asset for asset in queryset if (
                asset.nbi_data and asset.nbi_data["NBI_BRIDGE"]["Highway Agency District"] == value
            )
        ]

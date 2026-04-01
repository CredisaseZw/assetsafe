from django.contrib.contenttypes.models import ContentType
from apps.common.models.models import Address
from apps.companies.models import CompanyBranch
import django_filters


class CompanyBranchFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(method="filter_by_city")
    suburb = django_filters.CharFilter(method="filter_by_suburb")

    date_created_after = django_filters.DateFilter(
        field_name="date_created", lookup_expr="gte"
    )
    date_created_before = django_filters.DateFilter(
        field_name="date_created", lookup_expr="lte"
    )

    class Meta:
        model = CompanyBranch
        fields = ["company", "is_headquarters"]

    def filter_by_city(self, queryset, name, value):
        print(f"Filtering city: {value}")
        branch_content_type = ContentType.objects.get_for_model(CompanyBranch)
        return queryset.filter(
            addresses__content_type=branch_content_type,
            addresses__city__name__icontains=value,
        )

    def filter_by_suburb(self, queryset, name, value):
        branch_content_type = ContentType.objects.get_for_model(CompanyBranch)
        return queryset.filter(
            addresses__content_type=branch_content_type,
            addresses__suburb__name__icontains=value,
        )

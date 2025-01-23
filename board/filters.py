from django_filters import DateFilter, FilterSet, NumberFilter

from board import models


class AdvertisementFilter(FilterSet):
    """Фильтрация объявлений по диапазону цен, минимальной дате и авторам"""

    price_min = NumberFilter(field_name="price", lookup_expr="gte", label="Minimum price.")
    price_max = NumberFilter(field_name="price", lookup_expr="lte", label="Maxmum price.")
    min_date = DateFilter(field_name="created_at", lookup_expr="gte", label="Minimum creation date.")
    author = NumberFilter(lookup_expr="exact", label="The author of the ad.")

    class Meta:
        model = models.Advertisement
        fields = ()

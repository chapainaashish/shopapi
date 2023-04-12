from django_filters.rest_framework import FilterSet

from .models import Product


class ProductFilter(FilterSet):
    """A Product filterset class for custom filtering"""
    class Meta:
        model = Product
        fields = {"category_id": ["exact"], "price": ["lt", "gt"]}

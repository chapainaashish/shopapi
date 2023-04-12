from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from backends.pagination import DefaultPagination

from .filters import ProductFilter
from .models import Category, Product, Review
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializer import (
    CategorySerializer,
    ReadProductSerializer,
    ReadReviewSerializer,
    WriteProductSerializer,
    WriteReviewSerializer,
)


class ProductViewset(ModelViewSet):
    """A viewset for Product model"""

    queryset = Product.objects.annotate(average_rating=Avg("reviews__rating"))
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "average_rating"]
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        """Overriding to return serializer class based on HTTP request method"""
        if self.request.method == "GET":
            return ReadProductSerializer
        return WriteProductSerializer


class CategoryViewset(ModelViewSet):
    """A viewset for Category model"""

    queryset = Category.objects.annotate(total_products=Count("products"))
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ["total_products"]


class ReviewViewset(ModelViewSet):
    """A viewset for Review model"""

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [OrderingFilter]
    pagination_class = DefaultPagination
    ordering_fields = ["rating", "created_at"]

    def get_queryset(self):
        """Overriding for getting product specific reviews"""
        queryset = Review.objects.filter(product_id=self.kwargs["product_pk"])
        return queryset

    def get_serializer_context(self):
        """Overriding to return product pk for creating review"""
        return {
            "product_pk": self.kwargs["product_pk"],
            "user": self.request.user,
            "request": self.request,
        }

    def get_serializer_class(self):
        """Overriding to return serializer class based on HTTP request method"""
        if self.request.method == "GET":
            return ReadReviewSerializer
        return WriteReviewSerializer

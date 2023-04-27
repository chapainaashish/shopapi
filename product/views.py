from django.db.models import Avg, Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from backends.pagination import DefaultPagination
from backends.permission import IsAdminOrReadOnly

from .filters import ProductFilter
from .models import Category, Product, ProductImage, Review
from .permissions import IsAuthorOrReadOnly
from .serializer import (
    CategorySerializer,
    ProductImageSerializer,
    ReadProductSerializer,
    ReadReviewSerializer,
    WriteProductSerializer,
    WriteReviewSerializer,
)


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductViewset(ModelViewSet):
    """A viewset for Product model"""

    queryset = (
        Product.objects.annotate(average_rating=Avg("reviews__rating"))
        .select_related("category")
        .prefetch_related("images")
        .prefetch_related("reviews")
        .prefetch_related("reviews__user")
    )
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "average_rating"]
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        """Overriding to return serializer class based on HTTP method"""
        if self.request.method == "GET":
            return ReadProductSerializer
        return WriteProductSerializer


class ProductImageViewset(ModelViewSet):
    """A viewset for ProductImage model"""

    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """Overriding for getting product specific images"""
        return ProductImage.objects.filter(product=self.kwargs["product_pk"])

    def get_serializer_context(self):
        """Overriding to return product pk for uploading product image"""
        return {
            "product_pk": self.kwargs["product_pk"],
        }


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
        queryset = Review.objects.filter(
            product_id=self.kwargs["product_pk"]
        ).select_related("user")
        return queryset

    def get_serializer_context(self):
        """Overriding to return product pk for creating review"""
        return {
            "product_pk": self.kwargs["product_pk"],
            "user": self.request.user,
            "request": self.request,
        }

    def get_serializer_class(self):
        """Overriding to return serializer class based on HTTP method"""
        if self.request.method == "GET":
            return ReadReviewSerializer
        return WriteReviewSerializer

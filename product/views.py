from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from .models import Category, Product, Review
from .serializer import (
    CategorySerializer,
    ReadProductSerializer,
    ReadReviewSerializer,
    WriteProductSerializer,
    WriteReviewSerializer,
)


class ProductViewset(ModelViewSet):
    def get_queryset(self):
        """Overriding for filtering product with category"""
        category = self.request.query_params.get("category")
        queryset = Product.objects.prefetch_related("reviews").all()
        if category is not None:
            queryset = Product.objects.prefetch_related("reviews").filter(
                category__id=category
            )
        return queryset

    def get_serializer_class(self):
        """Overriding to return serializer class based on HTTP request method"""
        if self.request.method == "GET":
            return ReadProductSerializer
        return WriteProductSerializer


class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewset(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

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

    def perform_update(self, serializer):
        """Overriding to enforce user can only change his/her review"""
        review = self.get_object()
        if review.user != self.request.user:
            raise PermissionDenied(
                detail="You are not authorized to update this review"
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Overriding to enforce user can only delete his/her review"""
        if instance.user != self.request.user:
            raise PermissionDenied(
                detail="You are not authorized to delete this review"
            )
        instance.delete()

from rest_framework.viewsets import ModelViewSet

from .models import Category, Product, Review
from .serializer import CategorySerializer, ProductSerializer, ReviewSerializer


class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Overriding for filtering product with category"""
        category = self.request.query_params.get("category")
        queryset = Product.objects.all()
        if category is not None:
            queryset = Product.objects.filter(category__id=category)
        return queryset


class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewset(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Overriding for getting product specific reviews"""
        queryset = Review.objects.filter(product_id=self.kwargs["product_pk"])
        return queryset

    def get_serializer_context(self):
        """Overriding to return product pk for creating review"""
        return {
            "product_pk": self.kwargs["product_pk"],
            "user": self.request.user,
        }

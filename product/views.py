from rest_framework.viewsets import ModelViewSet

from .models import Category, Product, Review
from .serializer import CategorySerializer, ProductSerializer, ReviewSerializer


class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializer

    # filtering product with category
    def get_queryset(self):
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product_id"] = self.kwargs.get("pk")
        return context

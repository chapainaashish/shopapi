from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Product, Review
from .serializer import CategorySerializer, ProductSerializer, ReviewSerializer


@api_view()
def product_list(request):
    queryset = Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def product_details(request, id):
    return Response("ok")

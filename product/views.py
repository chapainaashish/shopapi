from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def product_list(request):
    return Response("ok")


@api_view()
def product_details(request, id):
    return Response("ok")

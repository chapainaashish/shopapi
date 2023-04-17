from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register(prefix="order", viewset=views.OrderViewset, basename="order")


orders_router = NestedDefaultRouter(router, "order", lookup="order")
orders_router.register("items", views.OrderItemViewset, basename="order-items")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(orders_router.urls)),
]

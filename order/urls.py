from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register(prefix="orders", viewset=views.OrderViewset, basename="order")

orders_router = NestedDefaultRouter(router, "orders", lookup="order")
orders_router.register("items", views.OrderItemViewset, basename="orders-item")


urlpatterns = router.urls + orders_router.urls

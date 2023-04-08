from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register("cart", views.CartViewset, basename="cart")

cart_router = routers.NestedDefaultRouter(router, "cart", lookup="cart")
cart_router.register("items", views.CartItemViewset, basename="cart-items")

urlpatterns = router.urls + cart_router.urls

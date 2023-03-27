from django.urls import path
from rest_framework_nested import routers as nrouter

from . import views

router = nrouter.DefaultRouter()
router.register(prefix="products", viewset=views.ProductViewset, basename="products")
router.register(prefix="category", viewset=views.CategoryViewset)


products_router = nrouter.NestedDefaultRouter(
    parent_router=router, parent_prefix="products", lookup="product"
)

products_router.register("reviews", views.ReviewViewset, basename="product-reviews")


urlpatterns = router.urls + products_router.urls

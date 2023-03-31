from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register(prefix="category", viewset=views.CategoryViewset)
router.register(prefix="products", viewset=views.ProductViewset, basename="product")


products_router = NestedDefaultRouter(
    parent_router=router, parent_prefix="products", lookup="product"
)

products_router.register("reviews", views.ReviewViewset, basename="product-reviews")


urlpatterns = router.urls + products_router.urls

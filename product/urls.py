from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register(prefix="category", viewset=views.CategoryViewset)
router.register(prefix="product", viewset=views.ProductViewset, basename="product")

# product/pk/reviews
# product/pk/images
products_router = NestedDefaultRouter(
    parent_router=router, parent_prefix="product", lookup="product"
)
products_router.register("reviews", views.ReviewViewset, basename="product-review")


products_router.register("images", views.ProductImageViewset, basename="product-image")


urlpatterns = router.urls + products_router.urls

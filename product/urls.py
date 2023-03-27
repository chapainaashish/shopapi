from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(prefix="product", viewset=views.ProductViewset)
router.register(prefix="category", viewset=views.CategoryViewset)

urlpatterns = router.urls

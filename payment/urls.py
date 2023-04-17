from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(prefix="payment", viewset=views.PaymentViewset, basename="order")

urlpatterns = router.urls

from rest_framework_nested.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("profile", views.ProfileViewset, "profile")
router.register("address", views.AddressViewset, "address")
router.register("payment", views.PaymentViewset, "payment")

urlpatterns = router.urls

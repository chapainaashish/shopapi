from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(prefix="payment", viewset=views.PaymentViewset, basename="order")

custom_urls = [
    path(
        "stripe/payment/create-checkout-session/<int:order_id>/",
        views.CreateStripeCheckoutSession.as_view(),
        name="checkout_session",
    ),
    path("webhooks/stripe/", views.StripeWebhookView.as_view(), name="stripe-webhook"),
]

urlpatterns = [
    path("", include(router.urls)),
    path("", include(custom_urls)),
]

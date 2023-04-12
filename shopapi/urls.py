from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("user/", include("customer.urls")),
    path("user/", include("cart.urls")),
    path("store/", include("product.urls")),
    path("store/", include("order.urls")),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

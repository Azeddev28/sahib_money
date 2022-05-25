

from django.contrib import admin
from django.urls import path, include  # add this

from apps.authentication import urls as authentication_urls
from apps.home import urls as home_urls
from apps.payments import urls as payment_urls

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include(authentication_urls)),
    path("payments/", include(payment_urls))             # UI Kits Html files
]



from django.contrib import admin
from django.urls import path, include  # add this

from apps.authentication import urls as authentication_urls
from apps.home import urls as home_urls

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include(authentication_urls)),
    path("", include(home_urls))             # UI Kits Html files
]

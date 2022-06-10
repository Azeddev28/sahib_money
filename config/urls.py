

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from apps.authentication import urls as authentication_urls
from apps.home import urls as home_urls
from apps.third_party_transaction import urls as tp_transaction_urls
from apps.wallet import urls as wallet_urls

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path('grappelli/', include('grappelli.urls')),
    path("tp-transaction/", include(tp_transaction_urls)),
    path("", include(authentication_urls)),
    path("", include(home_urls)),
    path("wallet/", include(wallet_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

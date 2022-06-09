

from django.urls import path

from apps.home.bindings import dashboard_view


urlpatterns = [
    path('', dashboard_view, name='home'),
]

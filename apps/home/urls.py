

from django.urls import path

from apps.home.bindings import dashboard_view, home_view


urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard', dashboard_view, name='dashboard'),
]

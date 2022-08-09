

from django.urls import path

from apps.home.bindings import dashboard_view, home_view, contact_us_view


urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard', dashboard_view, name='dashboard'),
    path('contact-us/', contact_us_view, name='contact-us'),
]

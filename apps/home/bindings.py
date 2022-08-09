from django.contrib.auth.decorators import login_required
from apps.authentication.decorators import authenticated_redirect

from apps.home.views import ContactUsView, DashboardView, HomeView


dashboard_view = login_required(DashboardView.as_view())
home_view = authenticated_redirect(HomeView.as_view())
contact_us_view = ContactUsView.as_view()

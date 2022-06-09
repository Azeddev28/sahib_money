from django.contrib.auth.decorators import login_required

from apps.home.views import DashboardView


dashboard_view = login_required(DashboardView.as_view())

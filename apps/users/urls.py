from django.urls import path

from apps.users.views import ProfileDetailsView


urlpatterns = [
    path('profile/', ProfileDetailsView.as_view(), name="profile"),
]

from django.urls import path

from apps.users.views import ProfileDetailsView, ResetPassword


urlpatterns = [
    path('profile/', ProfileDetailsView.as_view(), name="profile"),
    path('reset-password/', ResetPassword.as_view(), name='reset-password')
]

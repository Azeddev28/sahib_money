from django.urls import path

from apps.users.views import APIDetailsView, ProfileDetailsView, ResetPassword


urlpatterns = [
    path('profile/', ProfileDetailsView.as_view(), name="profile"),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('api-settings/', APIDetailsView.as_view(), name='api-settings'),

]

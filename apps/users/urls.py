from django.urls import path
from django.contrib.auth import views as auth_views

from apps.users.views import APIDetailsView, ProfileDetailsView, ResetPassword


urlpatterns = [
    path('profile/', ProfileDetailsView.as_view(), name="profile"),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('api-settings/', APIDetailsView.as_view(), name='api-settings'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/page_reset_password.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'), name='password_reset_complete'),
]

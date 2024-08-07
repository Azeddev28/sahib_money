import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.management.utils import get_random_secret_key
from django.contrib.auth.models import UnicodeUsernameValidator

from hashid_field import BigHashidAutoField

from apps.base_models import BaseModel
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username_validator = UnicodeUsernameValidator()

    email = models.CharField(
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, validate_email],
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    last_client_ip = models.CharField(max_length=100, default=None, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def credits(self):
        return '{:.2f}'.format(round(self.wallet.total_amount, 2))

    @property
    def account_type(self):
        if getattr(self, 'merchant_account', None):
            return 'Business Account'
        return 'Normal Account'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class MerchantAccount(BaseModel):
    merchant_app_key = BigHashidAutoField(primary_key=True, min_length=20)
    merchant_secret_key = models.CharField(max_length=64, default=get_random_secret_key)
    merchant_account_name = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='merchant_account')
    company_website = models.CharField(max_length=200)
    redirect_url = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.merchant_account_name

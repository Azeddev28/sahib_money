import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class MerchantAccount(BaseModel):
    account_name = models.CharField(max_length=40)
    merchant_secret_key = BigHashidAutoField(primary_key=True, min_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='merchant_account_user')
    company_website = models.CharField(max_length=200)

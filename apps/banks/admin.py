from django.contrib import admin

from apps.banks.models import UserBank


class UserBankModelAdmin(admin.ModelAdmin):
    class Meta:
        model = UserBank

    list_display = ('account_no', 'iban_no', 'account_name')

admin.site.register(UserBank, UserBankModelAdmin)

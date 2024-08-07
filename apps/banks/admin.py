from django.contrib import admin

from apps.banks.models import SahibMoneyBank, UserBank


class UserBankModelAdmin(admin.ModelAdmin):
    class Meta:
        model = UserBank

    list_display = ('user', 'account_number', 'iban_number', 'account_name')


class SahibMoneyBankModelAdmin(admin.ModelAdmin):
    class Meta:
        model = SahibMoneyBank

    list_display = ('account_number', 'iban_number', 'account_name')


admin.site.register(UserBank, UserBankModelAdmin)
admin.site.register(SahibMoneyBank, SahibMoneyBankModelAdmin)

from django.contrib import admin

from apps.payments.models import Payment


class PaymentModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Payment

    list_display = ['id', 'user', 'amount', 'status', 'created_at']
    readonly_fields = ['amount', 'receipt', 'user']


admin.site.register(Payment, PaymentModelAdmin)

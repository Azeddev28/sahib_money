from django.shortcuts import render
from django.views import View
from django.contrib import messages
from apps.banks.models import Bank

from apps.payments.forms import PaymentForm


class DepositPaymentView(View):
    def get(self, request, *args, **kwargs):
        form = PaymentForm
        bank = Bank.objects.filter(is_active=True).first()
        context = {'form': form, 'bank': bank}
        return render(request, 'payments/upload.html', context)

    def post(self, request, *args, **kwargs):
        bank = Bank.objects.filter(is_active=True).first()
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            form = PaymentForm
            context = {
                'form': form, 
                'bank': bank,
                'form_success': True
            }
            return render(request, 'payments/upload.html', context)

        messages.error(request, 'Invalid form submission.')
        messages.error(request, form.errors)
        form = PaymentForm
        context = {'form': form, 'bank': bank}
        return render(request, 'payments/upload.html', context)

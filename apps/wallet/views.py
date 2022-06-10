from django.shortcuts import render
from django.views import View
from django.contrib import messages

from apps.banks.models import SahibMoneyBank
from apps.wallet.forms import DepositForm


class DepositTransactionView(View):
    template_name = 'wallet/upload.html'

    def get(self, request, *args, **kwargs):
        form = DepositForm()
        bank = SahibMoneyBank.objects.filter(is_active=True).first()
        context = {'form': form, 'bank': bank}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        bank = SahibMoneyBank.objects.filter(is_active=True).first()
        form = DepositForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.wallet = request.user.wallet
            payment.save()

            form = DepositForm()
            context = {
                'form': form,
                'bank': bank,
                'form_success': True
            }
            return render(request, self.template_name, context)

        messages.error(request, 'Invalid form submission.')
        messages.error(request, form.errors)
        form = DepositForm()
        context = {'form': form, 'bank': bank}
        return render(request, self.template_name, context)

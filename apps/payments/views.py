from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib import messages

from apps.payments.forms import PaymentForm


class DepositPaymentView(View):
    def get(self, request, *args, **kwargs):
        form = PaymentForm
        return render(request, 'payments/upload.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            messages.success(request, 'Form submission successful. You will be notified in an hour')
            return HttpResponseRedirect("/")
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
            return HttpResponseRedirect("/")

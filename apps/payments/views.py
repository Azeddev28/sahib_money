from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PaymentForm

# Create your views here.
def deposit_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful. You will be notified in an hour')
            return HttpResponseRedirect("/") 
    else:
        form = PaymentForm
        
    return render(request, 'payments/upload.html', { 'form':form })
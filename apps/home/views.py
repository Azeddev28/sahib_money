

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views import View

from apps.wallet.models import Transaction


class DashboardView(View):
    template_name = 'home/dashboard.html'

    def get(self, request, *args, **kwargs):
        context = {
            'transactions': Transaction.objects.filter(wallet__user=request.user)
        }
        return render(request, self.template_name, context)

class HomeView(View):
    template_name = 'home/homepage_1.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

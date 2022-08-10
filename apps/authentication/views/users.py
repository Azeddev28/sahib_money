from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.views import View

from apps.authentication.decorators import authenticated_redirect
from apps.authentication.forms import LoginForm, SignUpForm
from apps.authentication.utils.login_utils import get_client_ip


User = get_user_model()


class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form,
        }

        if request.session.get('account_activated'):
            context['account_activated'] = True
            del request.session['account_activated']

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user: User = authenticate(email=email, password=password)
            if user is not None:
                ip_address = get_client_ip(request)
                user.last_client_ip = ip_address
                user.save()
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

        context = {
            "form": form,
            "msg": msg
        }
        return render(request, self.template_name, context)


class RegisterUserView(View):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        msg = None
        success = False
        form = SignUpForm()
        context = {'form': form, 'msg': msg, 'success': success}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            authenticate(email=email, password=raw_password)
            user.is_active = False
            user.save()
            msg = 'A verification email has been sent to your email. Please verify account in order to login.'
            success = True
        else:
            msg = 'Form is not valid'
            success = False

        context = {'form': form, 'msg': msg, 'success': success}
        return render(request, self.template_name, context)


class VerifyAccount(View):
    def get(self, request, uuid=None, *args, **kwargs):
        user = None
        try:
            user = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            return redirect('login')

        user.is_active = True
        user.save()
        request.session['account_activated'] = True
        return redirect('login')

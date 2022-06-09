from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.views import View

from apps.authentication.decorators import authenticated_redirect
from apps.authentication.forms import LoginForm, SignUpForm


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
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
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


@authenticated_redirect
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            authenticate(email=email, password=raw_password)
            user.is_active = False
            user.save()
            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


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

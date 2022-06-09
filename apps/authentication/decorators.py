from functools import wraps
from django.shortcuts import redirect


def authenticated_redirect(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        if(not request.user.is_authenticated):
            return function(request, *args, **kwargs)
        else:
            return redirect('/')

    return wrap

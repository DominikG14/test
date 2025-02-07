from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

import inspect, logging


def get_template(template_name: str = '', *, path: str = '', app: str) -> str:
    """Setups view template to render"""

    if not template_name:
        template_name = inspect.stack()[1][3] # Gets name of the function that this was called in
        template_name = template_name.replace('_', '-')

    if path:
        path = path.strip('/')
        return f'{app}/{path}/{template_name}.html'

    return f'{app}/{template_name}.html'


def unauthenticated_user(redirect_to: str = ''):
    """Restricts view for unauthenticated users only"""

    def decorator(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            else:
                return view_func(request, *args, **kwargs)
            
        return wrapper
    return decorator


def allowed_users(allowed_rolse: list, redirect_to: str = ''):
    """Restricts view for user with certain roles only"""

    def decorator(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_rolse:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(redirect_to)
            
        return wrapper
    return decorator
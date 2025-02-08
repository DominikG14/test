from django.http import HttpRequest
from django.shortcuts import redirect

import functools
import inspect


def get_template(template_name: str = '', *, path: str = '', app: str) -> str:
    """
    Constructs the path to a Django template based on provided parameters.

    Parameters
    ----------
    template_name : str, optional
        The name of the template file without extension. If not provided,
        the function name where this is called will be used (default is '').
    path : str, optional
        Additional path to be included in the template location (default is '').
    app : str
        The name of the Django app where the template is located.

    Returns
    -------
    str
        Full path to the template as a string.

    Notes
    -----
    - If `template_name` is not provided, the function dynamically uses the name of the calling function,
      replacing underscores with hyphens.
    - Trailing and leading slashes are removed from `path`.
    """

    if not template_name:
        template_name = inspect.stack()[1][3] # Gets name of the function that this was called in
        template_name = template_name.replace('_', '-')

    if path:
        path = path.strip('/')
        template = f'{app}/{path}/{template_name}.html'
    else:
        template = f'{app}/{template_name}.html'

    return template


def unauthenticated_only(redirect_to: str = ''):
    """
    Decorator to restrict view access to unauthenticated users only.

    Parameters
    ----------
    redirect_to : str, optional
        URL to redirect authenticated users to (default is '').

    Returns
    -------
    callable
        A decorator function for the view.

    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def role_required(allowed_roles: list[str], redirect_to: str = ''):
    """
    Decorator to restrict view access to users with specific roles only.

    Parameters
    ----------
    allowed_roles : list of str
        List of role names that are allowed to access the view.
    redirect_to : str, optional
        URL to redirect unauthorized users to (default is '').

    Returns
    -------
    callable
        A decorator function for the view.
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.user.groups.exists():
                roles = [group.name for group in request.user.groups.all()]

            if any(role in roles for role in allowed_roles):
                return view_func(request, *args, **kwargs)
            return redirect(redirect_to)
            
        return wrapper
    return decorator


def session_required(allowed_sessions: list[str], redirect_to: str = ''):
    """
    Decorator to restrict access to views only for users during specified sessions.

    Parameters
    ----------
    allowed_sessions : list of str
        List of session names that are allowed to access the view.
    redirect_to : str, optional
        URL to redirect if password reset session key is False (default is '').

    Returns
    -------
    callable
        A decorator function for the view.
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            if any(request.session.get(session, False) for session in allowed_sessions):
                return view_func(request, *args, **kwargs)
            return redirect(redirect_to)
        
        return wrapper
    return decorator
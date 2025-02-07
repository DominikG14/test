from django.http import HttpRequest
from django.shortcuts import redirect

import functools


USER_ACTIVATION_SESSION = 'user_activation'
PASSWORD_RESET_SESSION  = 'password_reset'


# def during_register(redirect_to: str = 'users:login'):
#     """
#     Decorator to restrict access to views only for users during registration.

#     Parameters
#     ----------
#     redirect_to : str, optional
#         URL to redirect if activation session key is False (default is 'users:login').

#     Returns
#     -------
#     callable
#         A decorator function for the view.
#     """

#     def decorator(view_func):
#         @functools.wraps(view_func)
#         def wrapper(request: HttpRequest, *args, **kwargs):
#             print(request.GET)
#             return view_func(*args, **kwargs)
        
#         return wrapper
#     return decorator

def during_register(redirect_to: str = 'users:login'):
    """
    Decorator to restrict access to views only for users during registration.

    Parameters
    ----------
    redirect_to : str, optional
        URL to redirect if activation session key is False (default is 'users:login').

    Returns
    -------
    callable
        A decorator function for the view.
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.session.get(USER_ACTIVATION_SESSION) == False:
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def during_password_reset(redirect_to: str = 'users:login'):
    """
    Decorator to restrict access to views only for users during password reset.

    Parameters
    ----------
    redirect_to : str, optional
        URL to redirect if password reset session key is False (default is 'users:login').

    Returns
    -------
    callable
        A decorator function for the view.
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.session.get(PASSWORD_RESET_SESSION) == False:
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator
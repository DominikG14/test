from django.http import HttpRequest

# Authentication
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Activation
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token

# Views
from django.shortcuts import render, redirect
from utils.views import get_template, session_required
from . import urls, forms


# Sessions
USER_ACTIVATION_SESSION = 'user_activation'
PASSWORD_RESET_SESSION  = 'password_reset'


# Authentication
def login(request: HttpRequest):
    template = get_template(app=urls.app_name)

    if request.method == 'GET':
        form = forms.LoginForm()

    if request.method == 'POST':
        form = forms.LoginForm(request.POST) 
        if form.is_valid():
            user = auth.authenticate(request,
                username=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password'),
            )
            if user:
                auth.login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('/users')

    return render(request, template, {
        'form': form
    })


@login_required
def logout(request):
    auth.logout(request)
    return redirect('users:login')



# Activation
def register(request: HttpRequest):
    template = get_template(app=urls.app_name)

    if request.method == 'GET':
        form = forms.RegisterForm()

    if request.method == 'POST': 
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.send_email_activation(request)
            request.session[USER_ACTIVATION_SESSION] = True
            return redirect('users:login')

    return render(request, template, {
        'form': form
    })


def activation_activate(request: HttpRequest, uidb64: str, token: str):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('users:activation_success')
    return redirect('users:activation_fail')


@session_required(USER_ACTIVATION_SESSION, redirect_to='users:login')
def activation_success(request: HttpRequest):
    try:
        del request.session[USER_ACTIVATION_SESSION]
    except KeyError:
        pass

    template = get_template(app=urls.app_name)
    return render(request, template)


@session_required(USER_ACTIVATION_SESSION, redirect_to='users:login')
def activation_fail(request: HttpRequest):
    try:
        del request.session[USER_ACTIVATION_SESSION]
    except KeyError:
        pass

    template = get_template(app=urls.app_name)
    return render(request, template)



# Password management
@login_required
def change_password(request: HttpRequest):
    template = get_template(app=urls.app_name)
    user = request.user

    if request.method == 'GET':
        form = forms.ChangePasswordForm(user)

    if request.method == 'POST':
        form = forms.ChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')

    return render(request, template, {
        'form': form
    })


def reset_password(request: HttpRequest):
    template = get_template(app=urls.app_name)
    if request.method == 'GET':
        form = forms.PasswordResetForm()

    if request.method == 'POST':
        form = forms.PasswordResetForm(request.POST)
        if form.is_valid():
            form.send_password_reset(request)
            request.session[PASSWORD_RESET_SESSION] = True
            return redirect('users:login')


    return render(request, template, {
        'form': form,
    })


def reset_password_reset(request: HttpRequest, uidb64: str, token: str):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if request.method == 'GET':
        form = forms.ChangePasswordForm(user)

    if request.method == 'POST':
        if user and account_activation_token.check_token(user, token):
            form = forms.ChangePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('users:reset_password_success')
        return redirect('users:reset_password_fail')
    
    template = get_template(app=urls.app_name)
    return render(request, template, {
        'form': form,
    })


@session_required(PASSWORD_RESET_SESSION, redirect_to='users:login')
def reset_password_success(request: HttpRequest):
    try:
        del request.session[PASSWORD_RESET_SESSION]
    except KeyError:
        pass
    
    template = get_template(app=urls.app_name)
    return render(request, template)


@session_required(PASSWORD_RESET_SESSION, redirect_to='users:login')
def reset_password_fail(request: HttpRequest):
    try:
        del request.session[PASSWORD_RESET_SESSION]
    except KeyError:
        pass

    template = get_template(app=urls.app_name)
    return render(request, template)
from django.http import HttpRequest

# Authentication
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Activation
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from .decorators import during_register, during_password_reset
from .decorators import USER_ACTIVATION_SESSION, PASSWORD_RESET_SESSION

# Views
from django.shortcuts import render, redirect
from utils.views import get_template
from . import urls, forms



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
                return redirect('/') #TODO: Add after login destination

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
            user = form.send_email_activation(request)
            request.session[USER_ACTIVATION_SESSION] = True
            return redirect('users:activation_send', to_email=user.email)

    return render(request, template, {
        'form': form
    })


@during_register
def activation_send(request: HttpRequest, to_email: str):
    template = get_template(app=urls.app_name)
    return render(request, template, {
        'to_email': to_email,
    })


@during_register
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


@during_register
def activation_success(request: HttpRequest):
    request.session[USER_ACTIVATION_SESSION] = False
    template = get_template(app=urls.app_name)

    return render(request, template)


@during_register
def activation_fail(request: HttpRequest):
    request.session[USER_ACTIVATION_SESSION] = False
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
            user = form.send_password_reset(request)
            request.session[PASSWORD_RESET_SESSION] = True
            return redirect('users:reset_password_send', to_email=user.email)


    return render(request, template, {
        'form': form,
    })


@during_password_reset
def reset_password_send(request: HttpRequest, to_email: str):
    template = get_template(app=urls.app_name)
    return render(request, template, {
        'to_email': to_email,
    })


@during_password_reset
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


@during_password_reset
def reset_password_success(request: HttpRequest):
    request.session[PASSWORD_RESET_SESSION] = False
    template = get_template(app=urls.app_name)

    return render(request, template)


@during_password_reset
def reset_password_fail(request: HttpRequest):
    request.session[PASSWORD_RESET_SESSION] = False
    template = get_template(app=urls.app_name)

    return render(request, template)
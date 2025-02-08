from django.http import HttpRequest
from . import models

# Mailing
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . import tokens

# Form creation
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  

    class Meta:  
        model = get_user_model() 
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
    
    def send_email_activation(self, request: HttpRequest,) -> models.User:
        user = self.save(commit=False)
        user.is_active = False
        user.save()

        subject = '' # TODO: Add subject
        message = render_to_string('users/activation-email.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': tokens.account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        })
        to_email = self.cleaned_data.get('email')
        email = EmailMessage(subject, message, to=[to_email])
        email.send()

        return user


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class PasswordResetForm(PasswordResetForm):
    def send_password_reset(self, request: HttpRequest) -> None:
        email = self.cleaned_data.get('email')
        user = get_user_model().objects.filter(email=email).first()
        if user:
            subject = '' # TODO: Add subject
            message = render_to_string('users/reset-password-email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': tokens.account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
            })
            email = EmailMessage(subject, message, to=[email])
            email.send()
        
        return user
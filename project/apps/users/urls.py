from django.urls import path
from . import views, redirects


app_name = 'users'
urlpatterns = []


PATHS = [
    # Authentication
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Activation
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activation_activate, name='activation_activate'),
    path('activate/success/', views.activation_success, name='activation_success'),
    path('activate/fail/', views.activation_fail, name='activation_fail'),

    # Password management
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_reset, name='reset_password_reset'),
    path('reset-password/success/', views.reset_password_success, name='reset_password_success'),
    path('reset-password/fail/', views.reset_password_fail, name='reset_password_fail'),
]

REDIRECTS = [
    path('', redirects.login),
]


urlpatterns += PATHS
urlpatterns += REDIRECTS
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect


def login(request: HttpRequest) -> HttpResponseRedirect:
    return redirect('users:login')
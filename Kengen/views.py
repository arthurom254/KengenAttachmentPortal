from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from .redirectings import redirecting
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = '/password-reset/done/'
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = '/password-reset/complete/'
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
def login(request):
    if request.user.is_authenticated:
        return redirecting(request)
    else:
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirecting(request)
            else:
                messages.info(request,"Invalid credentials")
                return redirect('/login')
        else:
            
            return render(request, 'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/login')
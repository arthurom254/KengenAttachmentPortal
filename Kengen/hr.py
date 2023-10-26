from django.shortcuts import render
from .forms import *
def hr(request):
    session=SessionForm
    context={
    'session':session,
    }
    return render(request,'hr.html', context)

"""This file is not used anywhere, tell arthur to remove it"""


from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
def redirecting(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        if user.groups.filter(name="Admin").exists():
            return redirect("/adm")
        elif user.groups.filter(name="supervisor").exists():
            return redirect("/supervisor?page=students")
        else:
            return redirect("/")
    else:
        return redirect("/login")

def studentredirect(request):
    if request.user.is_authenticated:
            user=User.objects.get(id=request.user.id)
            if user.groups.filter(name="Admin").exists():
                return redirect("/adm")
            elif user.groups.filter(name="supervisor").exists():
                return redirect("/supervisor?page=students")
            else:
                if request.user.is_superuser:
                    return redirect('/install')
                else:
                    return HttpResponse("The system has not yet been activated by the Administrator")
    else:
            return redirect("/login")
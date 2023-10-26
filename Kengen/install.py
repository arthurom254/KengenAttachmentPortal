from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.shortcuts import redirect

def new_group(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        if user.is_superuser:
            x, created=Group.objects.get_or_create(name='Admin')
            y, created=Group.objects.get_or_create(name='students')
            z, created=Group.objects.get_or_create(name='supervisor')
            if user.groups.filter(name='Admin').exists():
                pass
            else:
                x.user_set.add(user)
            return redirect('/')
        else:
            return redirect('/')
    
    else:
        return redirect('/login')
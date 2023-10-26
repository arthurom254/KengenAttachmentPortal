from .models import *
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .redirectings import redirecting
from django.contrib.auth.models import User
def make_session_active(id):
    actv=AttSession.objects.filter(active='True').update(active='False')
    actvive=AttSession.objects.get(id=id)
    actvive.active='True'
    actvive.save()
    return HttpResponse("Done")
def index(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        if user.groups.filter(name="supervisor").exists():
            try:
                page=request.GET['page']
            except:
                page='dashboard'
            if page == 'students':
                try:
                    stdid=request.GET['id']
                    users=User.objects.get(id=stdid)
                    std=Student.objects.get(student_details=users)
                    print("Pass test 1: try", stdid, users)
                    try:
                        print("We are in")
                        logid=request.GET['logs']
                        print("Pass test 1: logid:", logid)
                        logs=Logs.objects.get(id=logid)
                        if request.method=='POST':
                            approved=request.POST['approved']
                            logs.approved=approved
                            logs.comments=request.POST['comment']
                            logs.save()
                            string='/supervisor?page=students&id='+stdid+'&logs='+logid+'#comment'
                            return redirect(string)
                        else:
                            context={
                                'logs':logs,
                                'page_id':page,
                                'users':users,
                            }
                            print("Pass test 2: try: logid is here")
                            return render(request, 'supervisor/viewLogs.html', context)
                    except:
                        print("We are in 3 ==>")
                        logsb=Logs.objects.filter(student_details=std)
                        context={
                            'logs':logsb,
                            'page_id':page,
                            'stdid':stdid,
                            'users':users,
                            }
                        print("Pass test 3: try: no logid is here")
                        return render(request, 'supervisor/list.html', context)                    
                except:
                    profile,created=Supervisor.objects.get_or_create(supervisor_details=User(id=request.user.id))
                    students=Student.objects.filter(session=AttSession.objects.get(active='True'), department=profile.department)
                    departments=Department.objects.all()
                    context={
                        'students':students,
                        'profile':profile,
                        'page_id':page,
                        'departments':departments,
                    }
                    return render(request, 'supervisor/students.html', context)
            else:
                if request.method == 'POST':
                    fname=request.POST['fname']
                    lname=request.POST['lname']
                    email=request.POST['email']
                    phone=request.POST['phone']
                    profile,created=Supervisor.objects.get_or_create(supervisor_details=User(id=request.user.id))
                    if 'profile' in request.FILES:
                        image=request.FILES['profile']
                        fss=FileSystemStorage()
                        file=fss.save(f"profile/{image.name}", image)                
                        profile.profile_photo=file
                        profile.save()
                    profile.phone_number=phone
                    profile.save()
                    user=User.objects.get(id=request.user.id)
                    user.first_name=fname
                    user.last_name=lname
                    user.email=email
                    user.save()
                    return redirect('/supervisor')  
                else:
                    profile,created=Supervisor.objects.get_or_create(supervisor_details=User(id=request.user.id))
                    context={
                            'page_id':page,
                            'profile':profile,
                        }
                    return render(request, 'supervisor/weeks.html', context)
        else:
            return HttpResponse("Not permitted")
    else:
        return redirect("/login")
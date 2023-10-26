from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.db.models import Count
from .weeks import get_week_start_end_dates
from .mails import TemplateEmail
from .username import getUserName
def dashboard(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        if user.groups.filter(name="Admin").exists():
            try:
                page=request.GET['page']
            except:
                page='dashboard'
            departments=Department.objects.all()    
            if page == 'students':
                try:
                    try:
                        sessionid=request.GET['sid']
                        students=Student.objects.filter(session=AttSession(id=sessionid)).annotate(approved_count=Count('logs', filter=models.Q(logs__approved='True')))
                    except:
                        pass
                    try:
                        print("Pass test before, weekid")
                        wid=request.GET['wkid']
                        thisweek=Week.objects.get(id=wid)
                        print("Pass test after, weekid")
                        approvedlg=Logs.objects.filter(approved='True', week=thisweek)
                        print("Pass test after, approvedlogs as ", approvedlg)
                        context={
                            'approved': approvedlg,
                            'thisweek':thisweek,
                            'page_id':page,
                            }
                        print("Pass test context as", context)
                        return render(request, 'admin/students1.html', context)
                    except:
                        pass
                except:
                    students=Student.objects.filter(session=AttSession.objects.get(active='True')).annotate(approved_count=Count('logs', filter=models.Q(logs__approved='True')))
        
                try:
                    lid=request.GET['id']
                    users=User.objects.get(id=lid)
                    std=Student.objects.get(student_details=users)
                    try:
                        logid=request.GET['logs']
                        logs=Logs.objects.get(id=logid)
                        context={
                                'logs':logs,
                                'page_id':page,
                                'users':users,
                            }
                        return render(request, 'admin/viewLogs.html', context)
                    except:
                                                
                        logs=Logs.objects.filter(student_details=std, approved='True')
                        logs_reject=Logs.objects.filter(student_details=std, approved='False')
                        try:
                            report=FinalReport.objects.get(person=users).document
                        except:
                            report=None
                        context={
                            'logs': logs,
                            'users':users,
                        'page_id':page,
                        'report':report,
                        'logs_reject':logs_reject,
                        }
                        return render(request, 'admin/list.html', context)
                except:
                    try:
                        students=Student.objects.filter(session=AttSession.objects.get(active='True')).annotate(approved_count=Count('logs', filter=models.Q(logs__approved='True')))
                    except:
                        students=None
                    institutions=Institution.objects.all()
                    context={
                        'students':students,
                        'departments':departments,
                        'page_id':page,
                        'institutions':institutions,
                    }
                    return render(request, 'admin/students.html', context)
            elif page == 'supervisor':
                supervisor=Supervisor.objects.all()

                context={
                    'supervisor':supervisor,
                    'departments':departments,
                    'page_id':page,
                }
                return render(request, 'admin/supervisor.html', context)

            elif page == 'sessions':
                if request.method =='POST':
                    sess=request.POST['session']
                    actv=AttSession.objects.filter(active='True').update(active='False')
                    actvive=AttSession.objects.get(id=sess)
                    actvive.active='True'
                    actvive.save()
                    return redirect("/adm?page=%s" % page) 
                else:
                    sessions=AttSession.objects.all().order_by('active','startdate').reverse
                    context={
                        'sessions':sessions,
                        'page_id':page,
                    }
                    return render(request, 'admin/sessions.html', context)
            elif page == 'departments':
                    departments=Department.objects.all()
                    context={
                        'departments':departments,
                        'page_id':page,
                    }
                    return render(request, 'admin/department.html', context)
            elif page == 'institutions':
                institution=Institution.objects.all()
                context={
                        'institution':institution,
                        'page_id':page,
                    }
                return render(request, 'admin/institution.html', context)
            elif page == 'weeks':
                try:
                    close=request.GET['closed']
                    wid=request.GET['id']
                    if close == '0':
                        closed='False'
                    elif close == '1':
                        closed='True'
                    else:
                        closed=''
                    wk=Week.objects.get(id=wid)
                    wk.closed=closed
                    wk.save()
                    return redirect("/adm?page=%s" % page)
                except:
                    try:
                        weeks=Week.objects.filter(session=AttSession.objects.get(active='True'))
                    except:
                        weeks=None
                    context={
                            'weeks':weeks,
                            'page_id':page,
                        }
                    return render(request, 'admin/week.html', context)
            else:
                try:
                    student_count=Student.objects.filter(session=AttSession.objects.get(active='True')).count()
                except:
                    student_count=0
                session_count=AttSession.objects.all().count()
                supervisor_count=Supervisor.objects.all().count()
                department_count=Department.objects.all().count()
                context={
                    'page_id':page,
                    'student_count':student_count,
                    'session_count':session_count,
                    'supervisor_count':supervisor_count,
                    'department_count':department_count,
                }
                return render(request, 'admin/dashboard.html', context)
        else:
            return redirect("/")
    
    else:
        return redirect("/login")

def addnewuser(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user=User.objects.get(id=request.user.id)
            if user.groups.filter(name='Admin').exists():
                fname=request.POST['fname']
                lname=request.POST['lname']
                department=request.POST['department']
                username=request.POST['username']
                password=request.POST['password']
                password_confirmation=request.POST['password_confirmation']
                page=request.GET['page']
                if password_confirmation == password:
                    if User.objects.filter(username=username).exists():
                        messages.info(request,"User %s already exists" % username)
                        return redirect("/adm?page=%s" % page)
                    else:
                        newuser=User.objects.create_user(first_name=fname, last_name=lname, username=username, password=password)
                        newuser.save() 
                        if page == 'students':
                            group=Group.objects.get(name='students')
                            student, created=Student.objects.get_or_create( student_details= User(id=newuser.id), session=AttSession.objects.get(active='True'),department=Department(id=department)) 
                            group.user_set.add(newuser)
                            student.save()
                        elif page=='supervisor':
                            group=Group.objects.get(name='supervisor')
                            supervisor, created=Supervisor.objects.get_or_create( supervisor_details= User(id=newuser.id), department=Department(id=department) )
                            group.user_set.add( newuser)
                            supervisor.save()
                        return redirect("/adm?page=%s" % page)
                        
                else:
                    messages.error(request,"Password does not match")
                    return redirect("/adm?page=%s" % page)
            else:
                return redirect('/login')
        return HttpResponse(911)
    else:
        return redirect('/login')


def addNew(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        if user.groups.filter(name='Admin').exists():
            if request.method == 'POST':
                page=request.GET['page']
                if page == 'sessions':
                    startdate=request.POST['startdate']
                    enddate=request.POST['enddate']
                    week_dates = get_week_start_end_dates(startdate, enddate)
                    new, created=AttSession.objects.get_or_create(startdate=startdate, enddate=enddate)
                    new.save()
                    for week_number, start, end in week_dates:
                        # print("Week", week_number, "- Start:", start, "End:", end)
                        newweek=Week.objects.create(session=new, weeknum=week_number, startdate=start, enddate=end)
                        newweek.save()
                    return redirect("/adm?page=%s" % page)
                elif page == 'institutions':
                    institution_name=request.POST['institution_name']
                    insitution_campus=request.POST['institution_campus']
                    insitution_email=request.POST['insitution_email']
                    insitution_postbox=request.POST['institution_postbox']
                    newinst=Institution.objects.create(insitution_name=institution_name, insitution_campus=insitution_campus, insitution_email=insitution_email, insitution_postbox=insitution_postbox)
                    newinst.save()
                    return redirect("/adm?page=%s" % page)
                elif page == 'departments':
                    departments=request.POST['departments']
                    newdep=Department.objects.create(department_name=departments)
                    newdep.save()
                    return redirect("/adm?page=%s" % page)
                elif page == 'weeks':
                    startdate=request.POST['startdate']
                    enddate=request.POST['enddate']
                    weeknum=request.POST['weeknum']
                    new=Week.objects.create(startdate=startdate, enddate=enddate, weeknum=weeknum, session=AttSession.objects.get(active='True'))
                    new.save()
                    return redirect("/adm?page=%s" % page)
                else:
                    pass

        else:
            return HttpResponse("Not allowed")
    return redirect('/login')




def getApprovedStudents(request):
    students=Student.objects.annotate(approved_count=Count('Logs', filter=models.Q(logs__approved='True')))
    
    return HttpResponse(students)
"""""This is another version of adding new students: it sends an email to the student with username and password: Password 1 is the default password: """
def newProfile(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        if user.groups.filter(name='Admin'):
            if request.method == 'POST':
                fname=request.POST['fname']
                lname=request.POST['lname']
                department=request.POST['department']
                institution=request.POST['institution']
                email=request.POST['email']
                phone=request.POST['phone_number']
                username=getUserName(fname)
                if User.objects.filter(email=email).exists():
                    messages.info(request, f'user with email {email} already exist')
                else:
                    user=User.objects.create_user(username=username,password='Password1', email=email, first_name=fname, last_name=lname )
                    user.save()
                    group=Group.objects.get(name='students')
                    student, created=Student.objects.get_or_create( student_details= User(id=user.id), session=AttSession.objects.get(active='True'),department=Department(id=department), institution=Institution(id=institution), phone_number=phone) 
                    group.user_set.add(user)
                    student.save()
                    template=TemplateEmail(
                        to=email,
                        subject="Welcome",
                        template="welcome",
                        context={"fname":fname, "lname":lname, "username":username, "pwd":"Password1"},
                    )
                    template.send()
                return redirect('/adm?page=students')
        else:
            return redirect('/login')
    else:
        return redirect('/login')
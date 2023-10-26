from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from .forms import StudentForm
from .redirectings import studentredirect

def student_dashboard(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        if user.groups.filter(name="students").exists():
            form=StudentForm()
            student, created=Student.objects.get_or_create(student_details=User(id=request.user.id))
            try:
                supervisor=Supervisor.objects.filter(department=student.department)
            except:
                supervisor=None
            try:
                pdf=FinalReport.objects.get(person=User(id=request.user.id))
            except:
                pdf=None
            logs=Logs.objects.filter(student_details=student).order_by('week')
            weeks=Week.objects.filter(session=student.session, closed='False')
            inst=Institution.objects.all()
            context={
                'supervisors': supervisor,
                'weeks':weeks,
                'logs':logs,
                'student':student,
                'studentform':form,
                'institution':inst,
                'pdf':pdf,
            }
            return render(request, 'students/student_dashboard.html', context)
        else:
            return studentredirect(request)
    else:
        return redirect('/login')
    
def departmentActivation(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        if user.groups.filter(name="students").exists():
            if request.method == 'POST':
                institution=request.POST['institution']
                department=request.POST['department']
                student=Student.objects.get(student_details=User(id=request.user.id))
                student.department= Department(id=department)
                student.institution= Institution(id=institution)
                student.session=AttSession.objects.get(active='True') ######CHECK THIS
                student.save()
                return redirect('/')
    else:
        return redirect('/login')
   
def editLogs(request, id):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        std=Student.objects.get(student_details=user)
        if user.groups.filter(name="students").exists():
            if get_object_or_404(Week,id=id).closed == 'False': 
                logs,l=Logs.objects.get_or_create(student_details=std, week=Week(id=id))
                context={
                    'logs': logs,
                }
                return render(request, 'students/editLogs.html', context)
            else:
                return HttpResponse("Invalid request")
        return studentredirect(request)
    else:
        return redirect('/login')

    
def viewLogs(request, id):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        std=Student.objects.get(student_details=user)
        if user.groups.filter(name="students").exists():
            if get_object_or_404(Week,id=id): 
                logs,l=Logs.objects.get_or_create(student_details=std, week=Week(id=id))
                try:
                    nw=request.GET['new']
                    return redirect('/')
                except:
                    context={
                        'logs': logs,
                    }
                    return render(request, 'students/viewLogs.html', context)
            
        return studentredirect(request)
        
    else:
        return redirect("/login")
    

def saveLogs(request, id):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        std=Student.objects.get(student_details=user)
        if user.groups.filter(name="students").exists():
            if request.method == 'POST':
                activityDone= request.POST['activityDone']
                newSkillsAquired= request.POST['newSkillsAquired']
                challangesMet= request.POST['challangesMet']
                if get_object_or_404(Week,id=id): 
                    logs=Logs.objects.get(student_details=std, week=Week(id=id))
                    logs.activityDone= activityDone
                    logs.newSkillsAquired= newSkillsAquired
                    logs.challangesMet= challangesMet
                    logs.save()
                    return HttpResponse(True)
        return studentredirect(request)

    return redirect('/login')


def pdfLogs(request):
     if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        if user.groups.filter(name="students").exists():
            student=Student.objects.get(student_details=user)
            logs=Logs.objects.filter(student_details=student).order_by('week')
            context={
                'student':student,
                'pdflogs':logs
            }
            return render(request, 'students/pdf.html', context)
        else:
            return studentredirect(request)

def updateprofile(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        if user.groups.filter(name="students").exists():
            if request.method == 'POST':
                #fname=request.POST['fname']
                #lname=request.POST['lname']
                email=request.POST['email']
                phone=request.POST['phone']
                institution=request.POST['institution']
                finalreport,created=FinalReport.objects.get_or_create(person=User(id=request.user.id))
                if 'report' in request.FILES:
                    report=request.FILES['report']
                    fss=FileSystemStorage()
                    file=fss.save(f"documents/{report.name}", report)                
                    finalreport.document=file
                    finalreport.save()
                student, created=Student.objects.get_or_create( student_details = User(id=request.user.id))
                student.phone_number=phone
                student.institution=Institution(id=institution) 
                student.save()
                user=User.objects.get(id=request.user.id)
                #user.first_name=fname
                #user.last_name=lname
                user.email=email
                user.save()
                return redirect('/')  
        else:
            return studentredirect(request)
    else:
        return redirect('/login')
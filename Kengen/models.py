from django.db import models
from django.contrib.auth.models import User

TRUEFALSE=(
    ('True','True'),
    ('False','False'),
)


class Institution(models.Model):
    insitution_name=models.CharField(max_length=200)
    insitution_campus=models.CharField(max_length=200)
    insitution_email=models.CharField(max_length=100)
    insitution_postbox=models.CharField(max_length=100)
    def __str__(self):
        return f"{self.insitution_name} - {self.insitution_campus}"
    class Meta:
        ordering=['insitution_name','insitution_campus']

class Department(models.Model):
    department_name=models.CharField(max_length=200)

    def __str__(self):
        return f"{self.department_name} Department"
    class Meta:
        ordering=['department_name']
    
class AttSession(models.Model):
    startdate=models.DateField()
    enddate=models.DateField()  
    active=models.CharField(max_length=10, choices=TRUEFALSE, default='False')  
    def __str__(self):
        return f"{self.startdate} - {self.enddate}"
    
class Week(models.Model):
    session=models.ForeignKey(AttSession, on_delete=models.CASCADE)
    weeknum=models.IntegerField()
    startdate=models.DateField()
    enddate=models.DateField()
    closed=models.CharField(max_length=10, choices=TRUEFALSE, default='False')
    class Meta:
        ordering=['weeknum','session']
    
    def __str__(self):
        return f"Logs for {self.startdate} - {self.enddate}"
        
class Student(models.Model):
    student_details=models.ForeignKey(User, on_delete=models.CASCADE) #Fname, Lname, Uname, Email
    phone_number=models.CharField(max_length=15)
    institution=models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    session=models.ForeignKey(AttSession, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.student_details} - {self.institution}"
    
class Logs(models.Model):
    week=models.ForeignKey(Week, on_delete=models.CASCADE)
    student_details=models.ForeignKey(Student, on_delete=models.CASCADE)
    activityDone=models.TextField(max_length=2000,default='')
    newSkillsAquired=models.TextField(max_length=2000, default='')
    challangesMet=models.TextField(max_length=2000, default='')
    approved=models.CharField(max_length=10, choices=TRUEFALSE)
    comments=models.CharField(max_length=1000, null=True, blank=True)
#################################################3
    
    def __str__(self):
        return f"Logs for {self.week} Logs"    


class Supervisor(models.Model):
    supervisor_details=models.ForeignKey(User, on_delete=models.CASCADE)
    department=models.ForeignKey(Department, on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=15)
    profile_photo=models.ImageField(upload_to='supervisir', default='user.svg')
    session=models.ForeignKey(AttSession, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.supervisor_details} - {self.department}"

class FinalReport(models.Model):
    person=models.ForeignKey(User, on_delete=models.CASCADE)
    document=models.FileField(upload_to='documents')
    def __str__(self):
        return f"{self.person}'s Report"
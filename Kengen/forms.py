
from django import forms
from django.contrib.auth.models import User, Group
from .models import *
class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'password']

class GroupForm(forms.ModelForm):
    class Meta:
        model=Group
        fields='__all__'


class SessionForm(forms.ModelForm):
    class Meta:
        model=AttSession
        fields='__all__'


class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['department']

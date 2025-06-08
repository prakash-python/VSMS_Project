from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import StudentRegistration,Batch,mockperformance,weeklytest,Course
from django.core.exceptions import ValidationError
import re


class staff_form(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None  
        self.fields['password2'].help_text = None 

class staffregistration(UserCreationForm):
    email=forms.EmailField(required=True)
    
    is_staff=forms.BooleanField(required=False,label='Super Status')
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2','is_staff']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password1'].help_text=None
        self.fields['password2'].help_text=None
        self.fields['username'].help_text=None

class studentlogin(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

class batchform(forms.Form):
    Batchname=forms.CharField()
    Batchnumber=forms.CharField()

class courseform(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']

class StudentForm(forms.ModelForm):
    confirm_password = forms.CharField(label="Confirm Password",widget=forms.PasswordInput())
    class Meta:
        model=StudentRegistration
        fields=['first_name', 'last_name', 'email', 'password','confirm_password','batch','course','mobile_number', 'image']
        widgets = {
            'password': forms.PasswordInput(),
            
            'course':forms.Select(choices=StudentRegistration.course_choice) 
        }
        def __init__(self, *args, **kwargs):
            super(StudentForm, self).__init__(*args, **kwargs)
            self.fields['batch'].queryset = Batch.objects.all()

        def clean(self):
            cleaned_data=super().clean()
            password=cleaned_data.get("password")
            confirm_password=cleaned_data.get("confirm_password")
            if password!=confirm_password:
                self.add_error('confirm_password',"password and confirm password must be same")
            return cleaned_data

class studentidform(forms.Form):
    student_id=forms.CharField(label='Student_Id',max_length=1000)

class MockPerformance(forms.ModelForm):
    class Meta:
        model=mockperformance
        fields=['details','date']

class WeeklyTest(forms.ModelForm):
    class Meta:
        model = weeklytest
        fields = ['details','date']
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from . decorators import checksuperuser
from . forms import staff_form,courseform,batchform,studentlogin,staffregistration,StudentForm,MockPerformance,studentidform,WeeklyTest
from . models import Batch,StudentRegistration,mockperformance,weeklytest,attendance,PythonDeletedStudent,FrontEndDeletedStudent,MySQLDeletedStudent,Course
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
import datetime



# Create your views here.
def index(request):
    return render(request, 'index.html')

def stafflogin(request):
    error=None
    if request.method=='POST':
        form=staff_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
            except User.DoesNotExist:
                user = None
            
            if user is not None:
                login(request,user)
                return redirect('staffhomeurl')
            else:
                error='Invalid UserName Or Password'
                return render(request,'stafflogin.html',{'form':form,'error':error})
    else:
        form=staff_form()
    return render(request,'stafflogin.html',{'form':form,'error':error})



def create_batch(request, batch_name, batch_num):
    try:
        batch_details = Batch.objects.get(Batchname=batch_name, Batchnumber=batch_num)
        success_message = "Batch already exists."
    except Batch.DoesNotExist:
        new_batch = Batch(Batchname=batch_name, Batchnumber=batch_num)
        new_batch.save()
        success_message = "New batch created successfully."
        batch_details = new_batch
    students=batch_details.Student.all()
    return render(request, 'batchdetails.html', {'batch': batch_details, 'student_details':students, 'success': success_message})
def staff_registration(request):
    if request.method == 'POST':
        form = staffregistration(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data['is_staff']
            user.is_superuser = form.cleaned_data['is_staff']
            user.save()
            return redirect('stafflogin')  
    else:
        form = staffregistration()
    return render(request, 'staffregistration.html', {'form': form})
@checksuperuser
@login_required
def staffhome(request):
    if request.method == 'POST':
        b_form = batchform(request.POST)
        if b_form.is_valid():
            batch_name = b_form.cleaned_data['Batchname']
            batch_number = b_form.cleaned_data['Batchnumber']
            if 'create_batch' in request.POST:
                batch, created = Batch.objects.get_or_create(Batchname=batch_name, Batchnumber=batch_number)
                if created:
                    Group.objects.create(name=f'{batch.Batchname}-{batch.Batchnumber}')
                return redirect('batchdetails', batch_name=batch.Batchname, batch_number=batch.Batchnumber)
            elif 'get_details' in request.POST:
                try:
                    batch = Batch.objects.get(Batchname=batch_name, Batchnumber=batch_number)
                    return redirect('batchdetails', batch_name=batch.Batchname, batch_number=batch.Batchnumber)
                except Batch.DoesNotExist:
                    error = "Batch not found"
                    return render(request,'staffhome.html',{'form':b_form,'error':error})
            
        
    else:
        b_form = batchform()
    return render(request, 'staffhome.html', {'form': b_form})

def create_course(request):
    if request.method=='POST':
        form = courseform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staffhomeurl')
        else:
            form = courseform()
            return render(request,'create_course.html',{'form':form})
    return render(request,'create_course.html')

def stafflogout(request):
    auth_logout(request)
    return redirect('stafflogin')

def batchdata(request,batch_name,batch_number):
    batch=get_object_or_404(Batch,Batchname=batch_name,Batchnumber=batch_number)
    students=StudentRegistration.objects.filter(batch=batch)
    
    return render(request,'batchdetails.html',{
                                                'batchname':batch_name,
                                                'batchnumber':batch_number,
                                                'students':students})

def take_attendance(request, batch_name, batch_number):
    batch = get_object_or_404(Batch, Batchname=batch_name, Batchnumber=batch_number)
    students = StudentRegistration.objects.filter(batch=batch)
    
    if request.method == 'POST':
        selected_students_ids = request.POST.getlist('selected_students')
        
        for student in students:
            attendance_score = attendance.objects.filter(student=student).order_by('-student_id').first()
            
            if attendance_score:
                details_parts = attendance_score.details.split('/')
                attended_classes = int(details_parts[0])
                total_classes = int(details_parts[1]) + 1
                
                if str(student.id) in selected_students_ids:
                    attended_classes += 1
                    
                attendance_score.details = f"{attended_classes}/{total_classes}"
                attendance_score.save()
            else:
                if str(student.id) in selected_students_ids:
                    attendance_details = "1/1"
                else:
                    attendance_details = "0/1"
                
                attendance.objects.create(student=student, details=attendance_details)

        return redirect('batchdetails', batch_name=batch.Batchname, batch_number=batch.Batchnumber)

    return render(request, 'take_attendance.html', {'batch': batch,'batchname':batch_name,'batchnumber':batch_number, 'students': students})
@login_required
def get_mock_performance(request):
    if request.method == 'POST':
        form = studentidform(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            student = get_object_or_404(StudentRegistration, id=student_id)
            
            mock_performance = mockperformance.objects.filter(student=student).order_by('-date').first()
            if not mock_performance:
                mock_performance = mockperformance(student=student, details='', date=datetime.date.today())
                mock_performance.save()

            return render(request, 'mock_performance_details.html', {'student': student, 'mock_performance': mock_performance})
        else:
            return render(request, 'mock_performance.html', {'form': form, 'error': 'Invalid form data'})
    else:
        form = studentidform()
    return render(request, 'mock_performance.html', {'form': form})
@login_required
def update_mock_performance(request, student_id):
    student = get_object_or_404(StudentRegistration, id=student_id)
    mock_performance = mockperformance.objects.filter(student=student).order_by('-date').first()
    if request.method == 'POST':
        form = MockPerformance(request.POST, instance=mock_performance)
        if form.is_valid():
            mock_performance = form.save(commit=False)
            mock_performance.student = student  
            mock_performance.save()
            return render(request, 'mock_performance_details.html', {'student': student, 'mock_performance': mock_performance, 'message': 'Updated mock performance details'})
        else:
            print(form.errors)  
    else:
        form = MockPerformance(instance=mock_performance)
    return render(request, 'update_mock_performance.html', {'form': form, 'student': student})
@login_required
def get_weekly_test(request):
    if request.method=='POST':
        form=studentidform(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            student = get_object_or_404(StudentRegistration, id=student_id)
            
            weekly_test = weeklytest.objects.filter(student=student).order_by('-date').first()
            if not weekly_test:
                weekly_test = weeklytest(student=student, details='', date=datetime.date.today())
                weekly_test.save()

            return render(request, 'weekly_test_details.html', {'student': student, 'weekly_test': weekly_test})
        else:
            return render(request, 'weekly_test.html', {'form': form, 'error': 'Invalid form data'})
    else:
        form = studentidform()
        return render(request,'weekly_test.html',{'form':form})
@login_required
def update_weekly_test(request,student_id):
    student = get_object_or_404(StudentRegistration,id=student_id)
    weekly_test = weeklytest.objects.filter(student=student).order_by('-date').first()
    if request.method == 'POST':
        form = WeeklyTest(request.POST,instance=weekly_test)
        if form.is_valid():
            weekly_test = form.save(commit=False)
            weekly_test.student = student  
            weekly_test.save()
            return render(request, 'weekly_test_details.html', {'student': student, 'weekly_test': weekly_test, 'message': 'Updated weekly details'})
        else:
            print(form.errors)  
    else:
        form = WeeklyTest(instance=weekly_test)
        return render(request,'update_weekly_test.html',{'form':form})

def select_view(request,student_id):
    student=get_object_or_404(StudentRegistration,id=student_id)
    mock_performance=mockperformance.objects.filter(student=student).last()
    weekly_tests=weeklytest.objects.filter(student=student).last()
    attendence=attendance.objects.filter(student=student).last()
    context={
        'student':student,
        'mock_performance':mock_performance,
        'weekly_test':weekly_tests,
        'attendance':attendence
    }
    
    return render(request,'select.html',context)

def get_deleted_students(request):
    deleted_students = []
    selected_course = None
    if request.method == "POST":
        selected_course = request.POST.get("course_name")
        
        if selected_course == "python":
            deleted_students = PythonDeletedStudent.objects.all()
            
        elif selected_course == "Front-end":
            deleted_students = FrontEndDeletedStudent.objects.all()
        elif selected_course == "mysql":
            deleted_students = MySQLDeletedStudent.objects.all()
        else:
            deleted_students = []  
   
    return render(request, 'getdeletedstudents.html', {'deleted_students': deleted_students,'course': selected_course})

def student_login(request):
    if request.method == 'POST':
        form = studentlogin(request.POST)
        if form.is_valid():
            
            email = form.cleaned_data['email']
            
            password = form.cleaned_data['password']
            try:
                user = StudentRegistration.objects.get(email=email)
                user = authenticate(username=email, password=password)
            except StudentRegistration.DoesNotExist:
                user = None
            
            if user is not None and user.is_confirmed:
                
                login(request, user)
                return render(request,'student_details.html',{'student':user})
            else:
               
                return render(request, 'login.html', {'form':form,'error_message': 'Invalid credentials or account not confirmed.'})
    else:
        form = studentlogin()
    return render(request, 'login.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.password = make_password(form.cleaned_data['password'])
            send_mail_to_host(request, student)
            student.save()
            return redirect('student_login')
    else:
        form = StudentForm()
    return render(request, 'registration.html', {'form': form})

def send_mail_to_host(request, student):
    subject = 'New Student Registration'
    message = f'Dear staff,\n\nA new student has registered.\n\nName: {student.first_name} {student.last_name}\nEmail: {student.email}\n\nPlease review the registration.'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = settings.STAFF_EMAILS
    accept = f'http://{request.get_host()}/Vsms/accept/{student.email}/'
    reject = f'http://{request.get_host()}/reject/{student.email}/'
    html_message = f'''
    <p>Dear staff,</p>
    <p>A new student has registered.</p>
    <p>Name: {student.first_name} {student.last_name}</p>
    <p>Email: {student.email}</p>
    <p>Please review the registration.</p>
    <p><a href="{accept}" style="padding: 10px 15px; background-color: green; color: white; text-decoration: none;">Accept</a></p>

    <p><a href="{reject}" style="padding: 10px 15px; background-color: red; color: white; text-decoration: none;">Reject</a></p>
    '''
    msg = EmailMultiAlternatives(subject, message, from_email, to_email)
    msg.attach_alternative(html_message, "text/html")
    msg.send()

def send_confirmation_email(student):
    subject = 'Registration Accepted'
    message = f'Dear {student.first_name},\n\nYour registration has been accepted. You can now log in using your email and password.'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [student.email]
    html_message = f'''
    <p>Dear {student.first_name},</p>
    <p>Your registration has been accepted. You can now log in using your email and password.</p>
    <p><a href="http://127.0.0.1:8000/login/" style="padding: 10px 15px; background-color: blue; color: white; text-decoration: none;">Login</a></p>
    '''
    msg = EmailMultiAlternatives(subject, message, from_email, to_email)
    msg.attach_alternative(html_message, "text/html")
    msg.send()

def accept(request, email):
    student = get_object_or_404(StudentRegistration, email=email)
    student.is_confirmed = True
    print(student.is_confirmed)
    student.save()
    send_confirmation_email(student)
    return render(request, 'accept.html', {'student': student})
    
    

def reject(request, email):
    student = get_object_or_404(StudentRegistration, email=email)
    student.delete()
    return render(request, 'reject.html', {'email': email})

@login_required
def student(request):
    
    student = get_object_or_404(StudentRegistration, email=request.user.email)
    print('student in student view',student)
    return render(request, 'student_details.html', {'student': student})

def logout(request):
    auth_logout(request)
    return redirect('index')
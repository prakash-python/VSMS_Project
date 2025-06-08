from django.contrib import admin
from .models import Batch, StudentRegistration,mockperformance,weeklytest,attendance,PythonDeletedStudent,FrontEndDeletedStudent,MySQLDeletedStudent
# Register your models here.


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('Batchname', 'Batchnumber')

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'batch', 'course', 'is_confirmed')

@admin.register(mockperformance)
class MockPerformanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'details')
    search_fields = ('student__first_name', 'student__last_name')

@admin.register(weeklytest)
class WeeklyTestAdmin(admin.ModelAdmin):
    list_display = ('student', 'details')
    search_fields = ('student__first_name', 'student__last_name')

@admin.register(attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'details')
    search_fields = ('student__first_name', 'student__last_name')

@admin.register(PythonDeletedStudent)
class PythonDeletedStudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'course', 'deleted_at', 'attendance', 'mock_performance', 'weekly_test')
    search_fields = ('first_name', 'last_name', 'email', 'course')
    list_filter = ('course', 'deleted_at')

@admin.register(FrontEndDeletedStudent)
class FrontEndDeletedStudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'course', 'deleted_at', 'attendance', 'mock_performance', 'weekly_test')
    search_fields = ('first_name', 'last_name', 'email', 'course')
    list_filter = ('course', 'deleted_at')

@admin.register(MySQLDeletedStudent)
class MySQLDeletedStudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'course', 'deleted_at', 'attendance', 'mock_performance', 'weekly_test')
    search_fields = ('first_name', 'last_name', 'email', 'course')
    list_filter = ('course', 'deleted_at')
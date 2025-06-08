from rest_framework import serializers
from .models import Batch, Course, StudentRegistration, mockperformance, weeklytest, attendance

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['Batchname', 'Batchnumber']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name']

class StudentRegistrationSerializer(serializers.ModelSerializer):
    batch = BatchSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = StudentRegistration
        fields = [
            'first_name', 'last_name', 'email', 'batch', 'course',
            'mobile_number', 'image', 'is_confirmed'
        ]

class MockPerformanceSerializer(serializers.ModelSerializer):
    student = StudentRegistrationSerializer(read_only=True)

    class Meta:
        model = mockperformance
        fields = ['student', 'details', 'date']

class WeeklyTestSerializer(serializers.ModelSerializer):
    student = StudentRegistrationSerializer(read_only=True)

    class Meta:
        model = weeklytest
        fields = ['student', 'details', 'date']

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentRegistrationSerializer(read_only=True)

    class Meta:
        model = attendance
        fields = ['student', 'details']

# Serializers for DeletedStudent models
class PythonDeletedStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PythonDeletedStudent
        fields = [
            'student_id', 'first_name', 'last_name', 'email',
            'course', 'deleted_at', 'attendance', 'mock_performance', 'weekly_test'
        ]

class FrontEndDeletedStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontEndDeletedStudent
        fields = [
            'student_id', 'first_name', 'last_name', 'email',
            'course', 'deleted_at', 'attendance', 'mock_performance', 'weekly_test'
        ]

class MySQLDeletedStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MySQLDeletedStudent
        fields = [
            'student_id', 'first_name', 'last_name', 'email',
            'course', 'deleted_at', 'attendance', 'mock_performance', 'weekly_test'
        ]
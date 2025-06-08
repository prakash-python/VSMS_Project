from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
class Batch(models.Model):
    Batchname = models.CharField(max_length=100)
    Batchnumber = models.CharField(max_length=20)

    class Meta:
        unique_together = ('Batchname', 'Batchnumber')

    def __str__(self):
        return f'{self.Batchname} - {self.Batchnumber}'

class Course(models.Model):
    name =  models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class StudentManager(BaseUserManager):
    def create_user(self, email, password=None, **extrafields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extrafields):
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)

        if extrafields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extrafields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extrafields)


class StudentRegistration(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    course_choice = [
        ('python', 'Python'),
        ('Front-end', 'Front-end'),
        ('Full-stack', 'Full-stack'),
        ('mysql', 'MySQL'),
    ]
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'batch', 'course', 'mobile_number', 'image', 'is_confirmed']

    objects = StudentManager()

    def __str__(self):
        return self.first_name

    

class mockperformance(models.Model):
    student=models.ForeignKey(StudentRegistration,on_delete=models.CASCADE,null=True)
    details=models.TextField()
    date=models.DateField()
    def __str__(self):
        if self.student:
            return f"{self.student.last_name} - {self.details}"
        else:
            return f"Unknown Student - {self.details}"

class weeklytest(models.Model):
    student=models.ForeignKey(StudentRegistration,on_delete=models.CASCADE,null=True)
    details=models.TextField()
    date=models.DateField()

class attendance(models.Model):
    student=models.ForeignKey(StudentRegistration,on_delete=models.CASCADE,null=True)
    details=models.TextField()
    
class DeletedStudent(models.Model):
    student_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    course = models.CharField(max_length=100)
    deleted_at = models.DateTimeField(auto_now_add=True)
    attendance = models.CharField(max_length=100, default='0/0')
    mock_performance = models.CharField(max_length=100, default='0/0')
    weekly_test = models.CharField(max_length=100, default='0/0')

    class Meta:
        abstract = True
class PythonDeletedStudent(DeletedStudent):
    pass
class FrontEndDeletedStudent(DeletedStudent):
    pass

class MySQLDeletedStudent(DeletedStudent):
    pass

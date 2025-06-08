from django.contrib.auth.backends import ModelBackend
from .models import StudentRegistration

class StudentRegistrationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = StudentRegistration.objects.get(email=username)
            
            if user.check_password(password):
                return user
        except StudentRegistration.DoesNotExist:
            return None
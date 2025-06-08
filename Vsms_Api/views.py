from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from vsmsapp.models import StudentRegistration

@api_view(['POST'])
def student_login_jwt(request):
    email = request.data.get('username')  # frontend still sends as "username"
    password = request.data.get('password')

    try:
        student = StudentRegistration.objects.get(email=email)
    except StudentRegistration.DoesNotExist:
        return Response({'error': 'Invalid email or user not found'}, status=HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=student.email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'name': user.first_name,
            'email': user.email,
        }, status=HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=HTTP_400_BAD_REQUEST)

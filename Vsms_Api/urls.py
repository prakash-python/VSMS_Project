from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from Vsms_Api.views import *
urlpatterns=[
    
    path('login/', student_login_jwt),  # Updated view for JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
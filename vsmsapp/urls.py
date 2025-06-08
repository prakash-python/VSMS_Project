from django.urls import path
from . import views
urlpatterns=[
    path('', views.index, name='index'),    
    path('stafflogin/', views.stafflogin, name='stafflogin'),
    
    path('staffregister',views.staff_registration,name='staffregisterurl'),
    path('staffhomeurl/' , views.staffhome,name='staffhomeurl'),
    path('batchcreate/<str:batch_name>/<str:batch_num>/',views.create_batch,name='create_batch'),
    path('coursecreate/',views.create_course,name='course'),
    path('data/<str:batch_name>/<str:batch_number>/' ,views.batchdata,name='batchdetails'),
    path('batch/<str:batch_name>/<str:batch_number>/take_attendance/', views.take_attendance, name='take_attendance'),
    path('get_mock_performance/', views.get_mock_performance, name='get_mock_performance'),
    path('update_mock_performance/<int:student_id>/', views.update_mock_performance, name='update_mock_performance'),
    path('update_weekly_test/<int:student_id>/',views.update_weekly_test,name='update_weekly_test'),
    path('get_weekly_test/',views.get_weekly_test, name='get_weekly_test'),
    path('get_deleted_students/',views.get_deleted_students,name='get_deleted_students'),
    #path('delete/<int:student_id>/',views.delete_students,name='delete_student'),
    path('select/<int:student_id>/',views.select_view,name='selecturl'),
    path('stafflogout',views.stafflogout,name='stafflogouturl'),
    
    path('student_login/', views.student_login, name='student_login'),
    path('student_logout/', views.logout, name='logout'),
    path('student_sigin/', views.signin, name='signin'),
    path('accept/<str:email>/', views.accept, name='accept'),
    path('reject/<str:email>/', views.reject, name='reject'),
    path('student/', views.student, name='student_details'),

 ]


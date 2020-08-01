from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('class_details/<str:pk>', views.classDetails, name='class_details'),
    path('update_student/<str:pk>', views.updateStudent, name='update_student'),
    path('delete_student/<str:pk>', views.deleteStudent, name='delete_student'),

    path('create_class/', views.createClass, name='create-class'),
    path('create_user/', views.createUser, name='create-user'),
    path('create_student/', views.createStudent, name='create-student'),
    path('delete_class/<str:pk>', views.deleteClass, name='delete-class'),
    path('update_class/<str:pk>', views.updateClass, name='update-class'),

    path('student/', views.studentPage, name='student-page'),
    path('student_profile/<str:pk>', views.studentProfile, name='student-profile'),
    path('contact_form/', views.contactForm, name='contact-form'),
    path('student_update/<str:pk>', views.updateStudentForStudent, name='student-update'),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_complete'),


    path('pay/', views.payfee, name="pay"),
    path('charge/', views.charge, name="charge"),
    path('success/<str:args>/', views.successMsg, name="success"),


    path('generate_pdf/', views.GeneratePdf.as_view(), name='generatePdf'),
]
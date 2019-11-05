from django.urls import path
from MTP import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sLogin', views.sLogin, name='Login'),
    path('Dashboard', views.sDash, name='Dashboard'),
    path('fac_dash', views.fac_dash, name='Fac_Dash'),
    path("logout", views.logout_request, name="logout"),
    path("faculty", views.faculty_login, name="Faculty"),
    path("student_list", views.student_list, name="student_list"),
    path("create_student", views.create_student, name="create_student"),
    path("delete_student", views.delete_student, name="delete_student"),
    path("f_admin", views.f_admin, name="f_admin"),
    path("create_faculty", views.create_faculty, name="create_faculty"),
    path("create_course", views.create_course, name="create_course"),
    path("course_list", views.course_list, name="course_list"),
    path("subject_list", views.subject_list, name="subject_list"),
    path("create_subject", views.create_subject, name="create_subject"),
    path("test_list", views.test_list, name="test_list"),
    path("create_test", views.create_test, name="create_test"),
]
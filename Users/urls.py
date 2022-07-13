from django.urls import path
#from django.conf.urls import url
from . import views
app_name = 'Users'
urlpatterns = [
    #Home page
    path('',views.index, name='index'),

    #courses
    path('courses',views.courses,name = 'courses'),
    path('courses/my',views.my_courses,name='my_courses'),
    path('course/<slug:course_id>',views.course,name='course'),
    path('course/register/<slug:course_id>',views.register_for_course,name='register_for_course'),
    path('new_course',views.create_new_course, name='create_new_course'),
    path('edit_course/<slug:course_id>',views.edit_course,name='edit_course'),

    #auth
    path('login',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
    path('register',views.register_user,name='register_user'),
    path('register_instr',views.register_instructor,name='register_instructor'),
    path('register_student',views.register_student,name='register_student'),

    #profile
    path('profile/<slug:user_name>',views.view_profile,name = 'view_profile'),
    path('edit/profile',views.edit_profile,name='edit_profile'),

    #participants
    path('participants/<slug:course_id>', views.view_participants,name='view_participants'),
]
from django.urls import path
#from django.conf.urls import url
from . import views
app_name = 'Users'
urlpatterns = [
    #Home page
    path('',views.index, name='index'),
    path('courses',views.courses,name = 'courses'),
    path('courses/my',views.my_courses,name='my_courses'),
    path('course/<slug:course_id>',views.course,name='course'),
    path('course/register/<slug:course_id>',views.register_for_course,name='register_for_course'),
    path('new_course',views.create_new_course, name='create_new_course'),
    path('edit_course/<slug:course_id>',views.edit_course,name='edit_course'),
    path('login',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
]
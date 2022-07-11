from django.urls import path
#from django.conf.urls import url
from . import views
app_name = 'Users'
urlpatterns = [
    #Home page
    path('',views.index, name='index'),
    path('courses',views.courses,name = 'courses'),
    path('course/<slug:course_id>',views.course,name='course'),
    path('new_course',views.register_new_course, name='register_new_course'),
    path('login',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
]
from django.urls import path
#from django.conf.urls import url
from . import views
app_name = 'Users'
urlpatterns = [
    #Home page
    path('',views.index, name='index'),
    path('courses/<slug:course_name>',views.courses,name='courses'),
    path('login',views.login_user,name='login'),
    path('logout',views.logout_user,name='logout'),
]
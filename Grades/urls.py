from django.urls import path
#from django.conf.urls import url
from . import views
app_name = 'Grades'
urlpatterns = [
    
    path('course/<slug:course_id>',views.course_grade, name='course_grade'),
]
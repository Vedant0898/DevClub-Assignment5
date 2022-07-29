from django.urls import path
#from django.conf.urls import url
from . import views
app_name = 'Comms'
urlpatterns = [
    path('dm/',views.view_dm, name='view_dm'),
    path('dm/send',views.send_dm, name='send_dm'),
    
]
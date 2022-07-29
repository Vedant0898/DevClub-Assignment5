from django.urls import path
#from django.conf.urls import url
from . import views
app_name = 'Comms'
urlpatterns = [
    path('dm/',views.view_dm, name='view_dm'),
    path('dm/send',views.send_dm, name='send_dm'),
    path('announcements/<slug:course_id>',views.view_all_announcements,name = "view_all_announcements"),
    path('announcement/<slug:anc_id>',views.view_announcement,name='view_announcement'),
    path('announcement/<slug:anc_id>/del',views.delete_announcement,name="delete_announcement"),
    path('announcement/<slug:course_id>/new',views.new_announcement,name="new_announcement"),
    path('announcement/<slug:anc_id>/edit',views.edit_announcement,name="edit_announcement"),

]
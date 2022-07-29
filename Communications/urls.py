from django.urls import path
#from django.conf.urls import url
from . import views
app_name = 'Comms'
urlpatterns = [
    #dm
    path('dm/',views.view_dm, name='view_dm'),
    path('dm/send',views.send_dm, name='send_dm'),

    #announcement
    path('announcements/<slug:course_id>',views.view_all_announcements,name = "view_all_announcements"),
    path('announcement/<slug:anc_id>',views.view_announcement,name='view_announcement'),
    path('announcement/<slug:anc_id>/del',views.delete_announcement,name="delete_announcement"),
    path('announcement/<slug:course_id>/new',views.new_announcement,name="new_announcement"),
    path('announcement/<slug:anc_id>/edit',views.edit_announcement,name="edit_announcement"),

    #discussion forum
    path('discuss/<slug:course_id>',views.view_discussion,name="view_discussion"),
    path('discuss/<slug:course_id>/add',views.add_discussion,name = 'add_discussion'),
    path('discuss/<slug:disc_id>/edit',views.edit_discussion,name = "edit_discussion"),
    path('discuss/change_pin_status/<slug:disc_id>',views.change_pin_status,name='change_pin_status'),
    path('discuss/<slug:disc_id>/del',views.delete_discussion,name = "delete_discussion"),
    

]
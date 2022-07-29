from django.urls import path
#from django.conf.urls import url
from . import views
app_name = 'Docs'
urlpatterns = [
    path('view/<slug:course_id>',views.view_all_docs, name='all_docs'),
    path('delete/<slug:doc_id>',views.delete_doc,name='delete_doc'),
    path('add/<slug:course_id>',views.add_doc,name='add_doc'),
    path('edit/<slug:doc_id>',views.edit_doc,name='edit_doc'),

]
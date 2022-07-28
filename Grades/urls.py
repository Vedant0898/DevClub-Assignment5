from django.urls import path
#from django.conf.urls import url
from . import views
app_name = 'Grades'
urlpatterns = [
    
    path('course/<slug:course_id>',views.course_grade, name='course_grade'),
    path('assignments/<slug:course_id>',views.view_all_assignments,name='all_assignments'),
    path('assignment/<slug:assignment_id>',views.view_assignment,name='view_assignment'),
    path('assignment/edit/<slug:assignment_id>',views.edit_assignment,name='edit_assignment'),
    path('assignment/create/<slug:course_id>',views.create_assignment,name='create_assignment'),
    path('assignment/del/<slug:assignment_id>',views.delete_assignment,name='delete_assignment'),
    path('assignment/submit/<slug:assignment_id>',views.submit_assignment,name='submit_assignment'),
    path('assignment/resubmit/<slug:assignment_id>',views.resubmit_assignment,name='resubmit_assignment'),
    path('assignment/grade/<slug:a_sub_id>',views.grade_assignment,name='grade_assignment'),
    path('assignment/submissions/<slug:assignment_id>',views.view_all_assignment_submission,name='view_all_assignment_submission'),
    path('calc_total_grade/<slug:course_id>',views.calculate_total_grade,name='calculate_total_grade'),
    path('view_grade/<slug:course_id>',views.view_total_grades_instr,name='view_total_grade_instr'),



]
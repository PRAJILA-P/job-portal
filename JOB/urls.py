from django.urls import path
from . import views

app_name='job'

urlpatterns=[
    path('postjob/',views.post_job,name="postjob"),
    path('', views.job_list, name='joblist'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/edit/', views.edit_job, name='edit_job'),  # Edit job
    path('<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
]
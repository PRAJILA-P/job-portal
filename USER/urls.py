
from django.urls import  path

from . import views


app_name='user'

urlpatterns = [
    
    path('',views.index,name="index"),
    path('login/',views.login,name='login'),
    path('register/',views.register,name="register"),
    path('about/',views.about,name="about"),
    path('account/',views.account,name="account"),
    path('logout/', views.user_logout, name='logout'), 
    path('add_profile/',views.addprofile,name="addprofile"),
    path("edit-profile/", views.edit_profile, name="editprofile"),
    path('jobs/', views.view_jobs, name='view_jobs'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),

]

from django.urls import  path

from . import views


app_name='user'

urlpatterns = [
    
    path('', views.index, name="index"),
    path('login/',views.login,name='login'),
    path('register/',views.register,name="register"),
    path('about/',views.about,name="about"),
    path('account/',views.account,name="account"),
    path('logout/', views.user_logout, name='logout'), 
    path('add_profile/',views.addprofile,name="addprofile"),
    path("edit-profile/", views.edit_profile, name="editprofile"),
    path('jobs/', views.view_jobs, name='view_jobs'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('applications/', views.application_list, name='application_list'),
    path("applications/<int:pk>/", views.application_detail, name="application_detail"),

    # path('search/', views.job_search, name='job_search'),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<slug:slug>/", views.jobs_by_category, name="jobs_by_category"),


    path('service/',views.service,name="service"),
    path('faq/',views.faq,name="faq"),
    path('testimonials/',views.testimonials,name="testimonials"),
    path('blog/',views.blog,name="blog"),
    path('contact/',views.contact,name="contact"),
]
    

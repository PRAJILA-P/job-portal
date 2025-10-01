
from django.urls import  path

from . import views


app_name='recruiter'

urlpatterns = [
    
    path('login/',views.login,name="login"),
    path('register/',views.recruiter_register,name="register"),
    path('profile/', views.profile, name='profile'),
    # path('recruiter/profile/<int:recruiter_id>/', views.profile, name='profile'),

    path('logout/',views.logout,name="logout"),
    path("recruiter/<int:recruiter_id>/edit/", views.edit_profile, name="edit_profile"),

    # path('edit/profile/',views.edit_profile,name="edit_profile"),
    path('applications/', views.view_applications, name='view_applications'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
    path('application/<int:application_id>/update/', views.update_application_status, name='update_application_status'),

]
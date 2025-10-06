from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_resume, name='view_resume'),
    path('generate/', views.generate_resume, name='generate_resume'),
    path('add/projects/', views.add_project, name='add_project'),
]

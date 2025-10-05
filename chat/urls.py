from django.urls import path
from . import views
app_name = 'chat' 

urlpatterns = [
    path('start/<int:recruiter_id>/', views.start_chat, name='start_chat'),
    path('<str:room_name>/', views.chat_room, name='chat_room'),
]

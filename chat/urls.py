# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'  # <-- add this line for namespace

urlpatterns = [
    path("", views.index, name="index"),          # optional, for chat home
    path("<str:room_name>/", views.room, name="room"),  # name matches template
]

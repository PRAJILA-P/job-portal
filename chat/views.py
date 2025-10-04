from django.shortcuts import render

# Create your views here.

# def index(request):
#     return render(request, "chat/index.html")

# # Chat room
# def room(request, room_name):
#     # If no username provided, assign "Guest"
#     username = request.GET.get("username", "Guest")
#     return render(request, "chat/room.html", {
#         "room_name": room_name,
#         "username": username,
#     })


def index(request):
    return render(request, "chat/index.html")

# Specific chat room
def room(request, room_name):
    return render(request, "chat/room.html", {
        "room_name": room_name
    })
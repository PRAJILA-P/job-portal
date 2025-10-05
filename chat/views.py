from django.shortcuts import redirect,render, get_object_or_404

from RECRUITER.models import RecruiterRegister
from USER.models import JobSeeker
from .models import ChatRoom
from django.contrib.auth.decorators import login_required
from .models import ChatRoom


def start_chat(request, recruiter_id):
    # Make sure the user is logged in
    if 'jobseeker_id' not in request.session:
        return redirect('user:login')

    # Get the JobSeeker instance from session
    job_seeker_id = request.session['jobseeker_id']
    job_seeker = get_object_or_404(JobSeeker, id=job_seeker_id)

    # Get the Recruiter instance
    recruiter = get_object_or_404(RecruiterRegister, id=recruiter_id)

    # Create a unique room name: "jobseekerID_recruiterID"
    room_name = f"room_{job_seeker.id}_{recruiter.id}"

    # Get or create ChatRoom
    room, created = ChatRoom.objects.get_or_create(
        job_seeker=job_seeker,
        recruiter=recruiter,
        defaults={'room_name': room_name}
    )

    return redirect('chat:chat_room', room_name=room.room_name)



def chat_room(request, room_name):
    room = get_object_or_404(ChatRoom, room_name=room_name)
    
    # Determine current user ID (job seeker or recruiter)
    current_user_id = request.session.get('jobseeker_id') or request.session.get('recruiter_id')
    
    return render(request, 'chat/chat_room.html', {
        'room_name': room_name,
        'current_user_id': current_user_id  # pass it to template
    })

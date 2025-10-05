from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from django.contrib import messages

from JOB.models import JobApplication
from chat.models import ChatRoom

from . models import RecruiterProfile, RecruiterRegister
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
# Create your views here.




def recruiter_register(request):
    if request.method=="POST":
        company_name=request.POST.get("company_name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        website=request.POST.get("website")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request,"password do not match")
            return redirect("recruiter:register")

        
        if RecruiterRegister.objects.filter(email=email).exists():
            messages.error(request,"email already registered")
            return redirect("recruiter:register")
        register=RecruiterRegister(company_name=company_name,email=email,phone=phone,website=website,password=password)
        register.save()
        return redirect("recruiter:login")

    

    return render(request,'recruiter/register.html')

def login(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        try:
            recruiter=RecruiterRegister.objects.get(email=email)
        except RecruiterRegister.DoesNotExist:
            messages.error(request,"Invalid email") 
            return redirect("recruiter:login")
        
        if check_password(password,recruiter.password):
            request.session['recruiter_id']=recruiter.id
            request.session['company_name'] = recruiter.company_name
            request.session['email'] = recruiter.email
            request.session['phone'] = recruiter.phone
            request.session['website'] = recruiter.website
            request.session['created_at'] = recruiter.created_at.strftime("%Y-%m-%d %H:%M:%S")

            return redirect("recruiter:profile")
        else:
            messages.error(request,"invalid password")
            return redirect('recruiter:login')


    return render(request,'recruiter/login.html')
def profile(request):
    recruiter_id = request.session.get('recruiter_id')
    if not recruiter_id:
        return redirect("recruiter:login")  # Redirect if not logged in

    recruiter = get_object_or_404(RecruiterRegister, id=recruiter_id)
    profile = getattr(recruiter, 'profile', None)  # safe if profile exists
    chat_rooms = ChatRoom.objects.filter(recruiter=recruiter)
    context = {
        'recruiter': recruiter,
        'profile': profile,
        'recruiter_chat_rooms': chat_rooms
    }
    return render(request, 'recruiter/profile.html', context)


def logout(request):
    request.session.flush()
    return redirect('user:index')

def edit_profile(request, recruiter_id):
    recruiter = get_object_or_404(RecruiterRegister, id=recruiter_id)
    profile, created = RecruiterProfile.objects.get_or_create(recruiter=recruiter)

    if request.method == "POST":
        recruiter.company_name = request.POST.get("company_name")
        recruiter.email = request.POST.get("email")
        recruiter.phone = request.POST.get("phone")
        recruiter.website = request.POST.get("website")
        recruiter.save()

        profile.company_description = request.POST.get("company_description")
        profile.industry = request.POST.get("industry")
        profile.location = request.POST.get("location")
        profile.linkedin = request.POST.get("linkedin")
        
        # Handle empty established_date safely
        established_date = request.POST.get("established_date")
        profile.established_date = established_date if established_date else None

        if "logo" in request.FILES:
            profile.logo = request.FILES["logo"]

        profile.save()
        return redirect('recruiter:profile')

    return render(request, "recruiter/edit_profile.html", {
        'recruiter': recruiter,
        'profile': profile
    })

def view_applications(request):
    # Get recruiter ID from session
    recruiter_id = request.session.get('recruiter_id')
    if not recruiter_id:
        return redirect('recruiter:login')  # Redirect if not logged in

    # Get recruiter instance
    recruiter = get_object_or_404(RecruiterRegister, id=recruiter_id)

    # Filter only applications for jobs posted by this recruiter
    applications = JobApplication.objects.filter(
        job__recruiter=recruiter
    ).select_related('job_seeker', 'job_seeker__profile', 'job')

    

    context = {
        'applications': applications
    }
    return render(request, 'recruiter/ViewApplication.html', context)

# def view_applications(request):
#     # Get recruiter id from session
#     recruiter_id = request.session.get('recruiter_id')
#     if not recruiter_id:
#         return redirect('recruiter:login')

#     recruiter = get_object_or_404(RecruiterRegister, id=recruiter_id)

#     # Filter only applications for this recruiter
#     applications = JobApplication.objects.filter(job__recruiter=recruiter).select_related('job_seeker', 'job_seeker__profile', 'job')

#     context = {
#         'applications': applications
#     }
#     return render(request, 'recruiter/view_applications.html', context)


def application_detail(request, application_id):
    # Get recruiter id from session
    recruiter_id = request.session.get('recruiter_id')
    if not recruiter_id:
        return redirect('recruiter:login')

    recruiter = get_object_or_404(RecruiterRegister, id=recruiter_id)

    # Make sure the application belongs to this recruiter
    application = get_object_or_404(JobApplication, id=application_id, job__recruiter=recruiter)

    context = {
        'application': application
    }
    return render(request, 'recruiter/Application_details.html', context)


def update_application_status(request, application_id):
    recruiter_id = request.session.get('recruiter_id')
    if not recruiter_id:
        return redirect('recruiter:login')

    recruiter = get_object_or_404(RecruiterRegister, id=recruiter_id)
    application = get_object_or_404(JobApplication, id=application_id, job__recruiter=recruiter)

    if request.method == "POST":
        application.recruiter_notes = request.POST.get('recruiter_notes', '')
        application.status = request.POST.get('status', 'Pending')
        application.save()
        messages.success(request, "Application updated successfully!")
        return redirect('recruiter:application_detail', application_id=application.id)

    return redirect('recruiter:application_detail', application_id=application.id)


def chat(request):
    # Get the logged-in recruiter ID from session
    recruiter_id = request.session.get('recruiter_id')
    if not recruiter_id:
        return redirect("recruiter:login")  # Redirect if not logged in

    # Fetch the recruiter object
    recruiter = get_object_or_404(RecruiterRegister, id=recruiter_id)
    
    # Get all chat rooms where this recruiter is assigned
    recruiter_chat_rooms = ChatRoom.objects.filter(recruiter=recruiter).select_related('job_seeker')
    
    context = {
        'recruiter_chat_rooms': recruiter_chat_rooms
    }
    return render(request, 'recruiter/chat.html', context)

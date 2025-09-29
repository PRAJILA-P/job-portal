from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from USER.forms import JobSeekerForm, JobSeekerProfileForm
from JOB.models import Job
from .models import JobSeeker, JobSeekerProfile
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout

# Create your views here.


def index(request):
    return render(request,"user/home.html")

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Fetch the JobSeeker by email only
            jobseeker = JobSeeker.objects.get(email=email)
        except JobSeeker.DoesNotExist:
            messages.error(request,"Invalid email") 
            return redirect("user:login")


            # Check password
        if check_password(password, jobseeker.password):
                # Store details in session
            request.session['jobseeker_id'] = jobseeker.id
            request.session['jobseeker_name'] = jobseeker.full_name
            request.session['jobseeker_email'] = jobseeker.email
            request.session['jobseeker_phone'] = jobseeker.phone

            return redirect('user:account')
        else:
            messages.error(request, "Invalid password.")
            return render(request, 'user/login.html')

        
    return render(request, 'user/login.html')
# REGISTER VIEW
def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "user/register.html")

        if JobSeeker.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "user/register.html")

        # Save the user
        user = JobSeeker(
            full_name=full_name,
            email=email,
            phone=phone,
            password=password  # will be hashed in model's save()
        )
        user.save()
        # messages.success(request, "Registration successful! You can now log in.")
        return redirect('user:login')

    return render(request, "user/register.html")

def about(request):
    return render(request,"about.html")

def account(request):
    # Check if user is logged in
    jobseeker_id = request.session.get('jobseeker_id')
    if not jobseeker_id:
        return redirect("user:login")  # Redirect if not logged in

    # Fetch JobSeeker object
    jobseeker = get_object_or_404(JobSeeker, id=jobseeker_id)

    context = {
        'jobseeker': jobseeker
    }
    return render(request, 'user/account.html', context)

def user_logout(request):
    logout(request)  # clears the session
    return redirect('user:login')

def addprofile(request):
    jobseeker_id = request.session.get('jobseeker_id')
    if not jobseeker_id:
        messages.error(request, 'You need to login first')
        return redirect('user:login')

    jobseeker = get_object_or_404(JobSeeker, id=jobseeker_id)
    profile, _ = JobSeekerProfile.objects.get_or_create(user=jobseeker)

    if request.method == "POST":
        # File fields
        for f in ['profile_picture', 'resume']:
            if request.FILES.get(f):
                setattr(profile, f, request.FILES[f])

        # Other fields
        fields = ["dob","gender","address","education","certifications",
                  "preferred_job","employment_type","preferred_location",
                  "bio","skills","linkedin","github","portfolio","experience"]

        for field in fields:
            value = request.POST.get(field)
            if value:
                setattr(profile, field, value)

        profile.save()
        messages.success(request, "Profile saved successfully!")
        return redirect('user:account')

    return render(request, 'user/add_profile.html')

def edit_profile(request):
    jobseeker_id = request.session.get('jobseeker_id')  # get from session
    if not jobseeker_id:
        return redirect('user:login')  # redirect if not logged in

    jobseeker = get_object_or_404(JobSeeker, id=jobseeker_id)
    profile, created = JobSeekerProfile.objects.get_or_create(user=jobseeker)

    if request.method == "POST":
        jobseeker_form = JobSeekerForm(request.POST, instance=jobseeker)
        profile_form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)

        if jobseeker_form.is_valid() and profile_form.is_valid():
            jobseeker_form.save()
            profile_form.save()
            return redirect('user:account')
    else:
        jobseeker_form = JobSeekerForm(instance=jobseeker)
        profile_form = JobSeekerProfileForm(instance=profile)

    return render(request, "user/edit_profile.html", {
        "jobseeker_form": jobseeker_form,
        "profile_form": profile_form,
    })


def view_jobs(request):
    jobs=Job.objects.filter(is_active=True).order_by('-posted_at')
    return render(request,'user/view_job.html',{'jobs':jobs})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    return render(request, 'user/job_detail.html', {'job': job})
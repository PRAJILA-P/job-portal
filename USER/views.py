from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from USER.forms import JobSeekerForm, JobSeekerProfileForm
from JOB.models import Job, JobApplication
from CUSTOM_ADMIN.models import Category
from .models import JobSeeker, JobSeekerProfile
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.db.models import Q

# from RECRUITER.models import Region
# Create your views here.


# def index(request):
#     return render(request,"user/home.html")
# def index(request):
#     job_list = Job.objects.all().order_by('-id')  # latest jobs first
#     paginator = Paginator(job_list, 5)           # 5 jobs per page

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)   # handles invalid page numbers

#     return render(request, "user/home.html", {"jobs": page_obj})



# def index(request):
#     query = request.GET.get('query', '')       # job title or company name
#     location = request.GET.get('location', '') # location of the job
#     job_type = request.GET.get('job_type', '') # job type filter

#     # Start with active jobs
#     job_list = Job.objects.filter(is_active=True).order_by('-id')

#     # Filter by job title or company
#     if query:
#         job_list = job_list.filter(
#             Q(title__icontains=query) | Q(recruiter__company_name__icontains=query)
#         )

#     # Filter by location
#     if location:
#         job_list = job_list.filter(location__icontains=location)

#     # Filter by job type
#     if job_type:
#         job_list = job_list.filter(job_type=job_type)

#     # Pagination
#     paginator = Paginator(job_list, 5)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Job type dropdown
#     job_types = [choice[1] for choice in Job._meta.get_field('job_type').choices]

#     # Optional: you can create a list of unique locations from existing jobs
#     locations = Job.objects.values_list('location', flat=True).distinct()

#     context = {
#         'jobs': page_obj,
#         'locations': locations,
#         'job_types': job_types,
#         'selected_query': query,
#         'selected_location': location,
#         'selected_job_type': job_type,
#     }

#     return render(request, 'user/home.html', context)

# def index(request):
#     query = request.GET.get('query', '')       # job title or company name
#     location = request.GET.get('location', '') # location of the job
#     job_type = request.GET.get('job_type', '') # job type filter

#     # Start with active jobs
#     job_list = Job.objects.filter(is_active=True).order_by('-id')

#     # Title or company filter
#     if query:
#         job_list = job_list.filter(
#             Q(title__icontains=query) | Q(recruiter__company_name__icontains=query)
#         )

#     # Location filter (AND logic)
#     if location:
#         job_list = job_list.filter(location__icontains=location)

#     # Job type filter (AND logic)
#     if job_type:
#         job_list = job_list.filter(job_type=job_type)

#     # Pagination
#     paginator = Paginator(job_list, 5)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     # Dropdown data
#     job_types = [choice[1] for choice in Job._meta.get_field('job_type').choices]
#     locations = Job.objects.values_list('location', flat=True).distinct()

#     context = {
#         'jobs': page_obj,
#         'locations': locations,
#         'job_types': job_types,
#         'selected_query': query,
#         'selected_location': location,
#         'selected_job_type': job_type,
#     }

#     return render(request, 'user/home.html', context)


def index(request):
    query = request.GET.get('query', '')       # job title or company name
    location = request.GET.get('location', '') # location
    job_type = request.GET.get('job_type', '') # job type
    category_slug = request.GET.get('category', '') # category filter

    # Start with active jobs
    job_list = Job.objects.filter(is_active=True).order_by('-id')

    # Filter by title OR company
    if query:
        job_list = job_list.filter(
            Q(title__icontains=query) | Q(recruiter__company_name__icontains=query)
        )

    # Filter by location
    if location:
        job_list = job_list.filter(location__icontains=location)

    # Filter by job type
    if job_type:
        job_list = job_list.filter(job_type=job_type)

    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        job_list = job_list.filter(category=category)
    else:
        category = None

    # Pagination
    paginator = Paginator(job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Dropdown data
    job_types_choices = Job._meta.get_field('job_type').choices
    locations = Job.objects.values_list('location', flat=True).distinct()
    categories = Category.objects.all()

    context = {
        'jobs': page_obj,
        'locations': locations,
        'job_types_choices': job_types_choices,
        'categories': categories,
        'selected_query': query,
        'selected_location': location,
        'selected_job_type': job_type,
        'selected_category': category,
    }

    return render(request, 'user/home.html', context)


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
    jobs = Job.objects.filter(is_active=True).order_by('-posted_at')
    paginator = Paginator(jobs, 6)  # 6 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user/view_job.html', {'page_obj': page_obj})

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    return render(request, 'user/job_detail.html', {'job': job})

def application_list(request):
    jobseeker_id = request.session.get('jobseeker_id')
    if not jobseeker_id:
        return redirect('user:login')

    jobseeker = get_object_or_404(JobSeeker, id=jobseeker_id)

    # Only jobs this user applied for
    applications = JobApplication.objects.filter(job_seeker=jobseeker).order_by('-applied_on')

    return render(request, 'user/application_list.html', {'applications': applications})

def application_detail(request, pk):
    jobseeker_id = request.session.get('jobseeker_id')
    if not jobseeker_id:
        return redirect('user:login')

    jobseeker = get_object_or_404(JobSeeker, id=jobseeker_id)
    application = get_object_or_404(JobApplication, pk=pk, job_seeker=jobseeker)

    return render(request, 'user/application_details.html', {'application': application})


def category_list(request):
    categories = Category.objects.all()
    return render(request, "jobs/category_list.html", {"categories": categories})


def jobs_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    jobs = Job.objects.filter(categories=category, is_active=True).order_by('-id')  # ✅ use 'categories'

    context = {
        'category': category,
        'jobs': jobs,
    }
    return render(request, 'user/category.html', context)


def service(request):
    return render(request,'service.html')

def faq(request):
    return render(request,'faq.html')

def testimonials(request):
    return render(request,'testimonials.html')

def blog(request):
    return render(request,'blog.html')

def contact(request):
    return render(request,'contact.html')
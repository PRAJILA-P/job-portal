from django.shortcuts import get_object_or_404, redirect, render

from JOB.models import Job, JobApplication
from RECRUITER.models import RecruiterRegister
from django.contrib.auth.decorators import login_required

from USER.models import JobSeeker

# Create your views here.

def post_job(request):
    recruiter_id = request.session.get('recruiter_id')  
    recruiter = get_object_or_404(RecruiterRegister, id=recruiter_id)

    if request.method == "POST":
        Job.objects.create(
            recruiter=recruiter,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            requirements=request.POST.get("requirements"),
            roles_and_responsibilities=request.POST.get("roles_and_responsibilities"),
            education_required=request.POST.get("education_required"),
            location=request.POST.get("location"),
            job_type=request.POST.get("job_type"),
            salary=request.POST.get("salary") or None,
            experience_required=request.POST.get("experience_required"),
            deadline=request.POST.get("deadline") or None,
        )

        return redirect("job:joblist") 

    return render(request, 'recruiter/post_job.html')


def job_list(request):
    recruiter_id = request.session.get('recruiter_id')
    
    if not recruiter_id:
        # if recruiter not in session, show empty or redirect
        return redirect('recruiter:login')  # or just return an empty list
    
    recruiter = RecruiterRegister.objects.get(id=recruiter_id)
    jobs = Job.objects.filter(recruiter=recruiter)

    return render(request, 'recruiter/job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'recruiter/job_detail.html', {'job': job})

def edit_job(request, job_id):
    # First, get the job object
    job = get_object_or_404(Job, id=job_id)

    recruiter_id = request.session.get('recruiter_id')
    
    # Ensure the logged-in recruiter owns this job
    if job.recruiter.id != recruiter_id:
        return redirect('job:joblist')  # early return is fine because job is already defined

    if request.method == "POST":
        job.title = request.POST.get("title")
        job.description = request.POST.get("description")
        job.requirements = request.POST.get("requirements")
        job.roles_and_responsibilities = request.POST.get("roles_and_responsibilities")
        job.education_required = request.POST.get("education_required")
        job.location = request.POST.get("location")
        job.job_type = request.POST.get("job_type")
        job.salary = request.POST.get("salary") or None
        job.experience_required = request.POST.get("experience_required")
        job.deadline = request.POST.get("deadline") or None
        job.save()
        return redirect('job:job_detail', job_id=job.id)

    # If GET request, render form with job object
    return render(request, 'recruiter/edit_job.html', {'job': job})

def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    recruiter_id = request.session.get('recruiter_id')
    
    # Ensure the logged-in recruiter owns this job
    if job.recruiter.id == recruiter_id:
        job.delete()
    
    return redirect('job:joblist')

def apply_job(request, job_id):
    # Manual authentication check
    if 'jobseeker_id' not in request.session:
        return redirect('user:login')  # Redirect if not logged in

    try:
        job_seeker = JobSeeker.objects.get(id=request.session['jobseeker_id'])
    except JobSeeker.DoesNotExist:
        return redirect('user:login')

    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        cover_letter = request.POST.get('cover_letter')

        # Create JobApplication
        JobApplication.objects.create(
            job_seeker=job_seeker,
            job=job,
            phone_number=phone_number,
            cover_letter=cover_letter,
            status='Applied'
        )

        return redirect('user:job_detail', job_id=job.id)  # Redirect to dashboard

    context = {
        'job': job,
        'job_seeker': job_seeker,
    }
    return render(request, 'user/apply_job.html', context)
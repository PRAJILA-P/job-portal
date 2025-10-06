from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
from USER.models import JobSeekerProfile
from .models import Project  # replace with your app name

def view_resume(request):
    # Get JobSeeker ID from session
    jobseeker_id = request.session.get("jobseeker_id")
    if not jobseeker_id:
        return redirect("user:login")  # redirect if not logged in

    # Get profile
    profile = get_object_or_404(JobSeekerProfile, user__id=jobseeker_id)

    # Render HTML template
    return render(request, 'resume/resume_view.html', {'profile': profile})

def generate_resume(request):
    jobseeker_id = request.session.get("jobseeker_id")
    if not jobseeker_id:
        return redirect("user:login")

    profile = get_object_or_404(JobSeekerProfile, user__id=jobseeker_id)

    # Local background image path
    background_path = r'C:\path\to\media\resume_bg.jpg'  # full path to your background image

    html = render_to_string('resume/resume_template.html', {
        'profile': profile,
        'background_path': background_path
    })

    config = pdfkit.configuration(
        wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    )

    options = {
        'enable-local-file-access': None,
        'load-error-handling': 'ignore',
        'load-media-error-handling': 'ignore',
    }

    pdf = pdfkit.from_string(html, False, configuration=config, options=options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{profile.user.full_name}_resume.pdf"'
    return response


def add_project(request):
    # Get jobseeker ID from session (if you're storing it that way)
    jobseeker_id = request.session.get("jobseeker_id")

    # Redirect to login if not found
    if not jobseeker_id:
        return redirect("user:login")

    # Get the user's profile
    profile = get_object_or_404(JobSeekerProfile, user__id=jobseeker_id)

    # Fetch all projects belonging to the profile
    projects = Project.objects.filter(profile=profile)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        technologies = request.POST.get('technologies')
        link = request.POST.get('link')

        # Create a new project entry
        Project.objects.create(
            profile=profile,
            title=title,
            description=description,
            technologies=technologies,
            link=link
        )

        # Redirect back to the same page so user can add more
        return redirect('add_project')

    return render(request, 'resume/add_project.html', {'projects': projects})
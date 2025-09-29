from django import forms
from .models import JobSeeker, JobSeekerProfile

class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['full_name', 'email', 'phone']  # don’t include password here

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = [
            'profile_picture', 'dob', 'gender', 'address', 'education',
            'certifications', 'preferred_job', 'employment_type',
            'preferred_location', 'resume', 'bio', 'skills',
            'linkedin', 'github', 'portfolio', 'experience'
        ]

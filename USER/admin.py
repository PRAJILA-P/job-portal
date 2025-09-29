from django.contrib import admin

from .models import JobSeeker, JobSeekerProfile

# Register your models here.

admin.site.register(JobSeeker)
admin.site.register(JobSeekerProfile)
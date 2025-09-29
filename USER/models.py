from django.db import models
from django.contrib.auth.hashers import make_password

class JobSeeker(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # store hashed password
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    

from django.db import models

class JobSeekerProfile(models.Model):
    EMPLOYMENT_CHOICES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('IN', 'Internship'),
        ('CT', 'Contract'),
        ('FR', 'Freelance'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField("JobSeeker", on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="user/profile_pics/", blank=True, null=True)

    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    address = models.CharField(max_length=255, blank=True, null=True)
    education = models.TextField(blank=True, null=True)  # you can normalize later into another model if needed
    certifications = models.TextField(blank=True, null=True)

    preferred_job = models.CharField(max_length=150, blank=True, null=True)
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_CHOICES, blank=True, null=True)
    preferred_location = models.CharField(max_length=150, blank=True, null=True)

    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)  # comma-separated or JSON
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)  # optional

    experience = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name}'s Profile"



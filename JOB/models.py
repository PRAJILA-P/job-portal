from django.db import models
from RECRUITER.models import RecruiterRegister
from USER.models import JobSeeker
# Create your models here.


class Job(models.Model):
    recruiter = models.ForeignKey(RecruiterRegister, 
        on_delete=models.CASCADE, 
        related_name="jobs"
    )
    title = models.CharField(max_length=200)  # e.g. Python Developer
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)  # skills needed
    roles_and_responsibilities = models.TextField(
        blank=True,
        null=True,
        help_text="Add roles and responsibilities (separate by new lines)."
    )
    education_required = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="E.g. Bachelor's in CS, MBA, or any qualification."
    )
    location = models.CharField(max_length=200)
    job_type = models.CharField(
        max_length=50,
        choices=[
            ("FT", "Full-Time"),
            ("PT", "Part-Time"),
            ("IN", "Internship"),
            ("CT", "Contract"),
            ("FR", "Freelance"),
        ],
        default="FT",
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    experience_required = models.CharField(max_length=100, blank=True, null=True)  # e.g. "2-4 years"
    posted_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(blank=True, null=True)  # application deadline
    is_active = models.BooleanField(default=True)  # recruiter can deactivate job

    def __str__(self):
        return f"{self.title} at {self.recruiter.company_name}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Interview', 'Interview Scheduled'),
        ('Hired', 'Hired'),
    ]

    # The job seeker who applied
    job_seeker = models.ForeignKey(
        JobSeeker, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    
    # The job being applied to
    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    
 
    # Optional cover letter
    cover_letter = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True) 
    
    # Timestamp of when the application was made
    applied_on = models.DateTimeField(auto_now_add=True)

    # Notes by recruiter
    recruiter_notes = models.TextField(blank=True, null=True)
    
    # Current status of the application
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')

    def __str__(self):
        return f"{self.job_seeker.full_name} - {self.job.title} - {self.status}"

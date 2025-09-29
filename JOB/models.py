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


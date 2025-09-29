from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class RecruiterRegister(models.Model):
    company_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    phone = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.pk:
            self.password=make_password(self.password)
        super().save(*args,**kwargs)    

    def __str__(self):
        return self.company_name


class RecruiterProfile(models.Model):
    recruiter = models.OneToOneField(
        RecruiterRegister,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    
    company_description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.recruiter.company_name} Profile"



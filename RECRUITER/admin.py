from django.contrib import admin

from .models import RecruiterProfile, RecruiterRegister

# Register your models here.

admin.site.register(RecruiterRegister)

admin.site.register(RecruiterProfile)
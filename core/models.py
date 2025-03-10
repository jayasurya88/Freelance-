from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    ]

    # Common Fields for All Users
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    country = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)  # OTP field
    verified = models.BooleanField(default=False) 
    # Freelancer-Specific Fields
    professional_title = models.CharField(max_length=100, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    experience_level = models.CharField(max_length=100, blank=True, null=True)  # Beginner/Intermediate/Expert
    portfolio = models.URLField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    availability_status = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Available", "Not Available"
    preferred_tools = models.TextField(blank=True, null=True)

    # Client-Specific Fields
    company_name = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    project_budget = models.CharField(max_length=100, blank=True, null=True)
    project_frequency = models.CharField(max_length=100, blank=True, null=True)  # e.g., "One-time", "Recurring"
    company_size = models.CharField(max_length=100, blank=True, null=True)

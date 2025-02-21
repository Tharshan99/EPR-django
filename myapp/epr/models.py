from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinLengthValidator


# Custom User Model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email

class JobVacancy(models.Model):
    job_title = models.CharField(max_length=255)
    job_details = models.TextField()
    closing_date = models.DateField()
    qualifications = models.TextField()  # Rich text field for qualifications
    requirements = models.TextField()    # Rich text field for requirements
    location = models.CharField(max_length=255)
    pay_details = models.CharField(max_length=255)
    FULL_TIME = 'FT'
    PART_TIME = 'PT'
    JOB_TYPE_CHOICES = [
        (FULL_TIME, 'Full Time'),
        (PART_TIME, 'Part Time'),
    ]
    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES, default=FULL_TIME)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.job_title
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.utils.text import slugify


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
    
class JobApplication(models.Model):
    job = models.ForeignKey(JobVacancy, on_delete=models.CASCADE, related_name='applications')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    confirm_email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    place_of_residence = models.CharField(max_length=100)
    message = models.TextField()
    cv = models.FileField(upload_to='cvs/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job.job_title}"
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    img_url = models.ImageField(null=True, upload_to='posts/images')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
   
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def formatted_img_url(self):
        url = self.img_url if self.img_url.__str__().startswith(("http", "https")) else self.img_url.url
        return url
   
    def __str__(self):
        return self.title
    

#################
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
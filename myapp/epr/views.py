from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm, RegisterForm, JobVacancyForm
from django.contrib.auth import login as auth_login, authenticate, get_user_model
from .models import Contact, JobVacancy


User = get_user_model()  # This will dynamically use your custom user model


# Create your views here.
def index(request):
    return render(request, 'epr/index.html')

def detail(request):
    return HttpResponse("Hello welcome to detail page")

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_entry = form.save()  # Save form data to database

            # Prepare email details
            subject = "Thank You for Contacting EPR Groupers"
            message = f"""
            Hello {contact_entry.name},

            Thank you for reaching out to us at EPR Groupers! 
            We have received your message and will get back to you as soon as possible.

            Here are the details you submitted:
            ---------------------------------
            Name: {contact_entry.name}
            Email: {contact_entry.email}
            Contact: {contact_entry.contact}
            Message: {contact_entry.message}
            ---------------------------------

            If you need immediate assistance, feel free to contact us at support@eprgroupers.com.

            Best Regards,
            EPR Groupers Team
            """

            from_email = "noreply@eprgroupers.com"
            recipient_list = [contact_entry.email]  # Send email to the submitted contact email

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, "Your message has been submitted successfully! A confirmation email has been sent.")
            except Exception as e:
                messages.error(request, f"Your message was submitted, but we could not send an email. Error: {e}")

            return redirect('epr:contact')  # Redirect back to the contact page

    else:
        form = ContactForm()

    return render(request, "epr/contact.html", {"form": form})

# def login(request):
#     return render(request, 'epr/login.html')

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        # Authenticate using email instead of username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)  # Logs in the user
            messages.success(request, "You have successfully logged in!")
            return redirect("epr:dashboard")  # Redirect to the user's dashboard/homepage
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, "epr/login.html")

def dashboard(request):
    return render(request, 'epr/dashboard.html')

def career_dashboard(request):
    return render(request, 'epr/career_dashboard.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # ✅ Pass both request and user
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect("epr:login")  # Change this to your desired page
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterForm()
    
    return render(request, "epr/register.html", {"form": form})

def contact_dashboard(request):
    contacts = Contact.objects.all().order_by('-created_at')  # Fetch latest first
    return render(request, 'epr/contact_dashboard.html', {'contacts': contacts})

def career(request):
    published_jobs = JobVacancy.objects.filter(published=True)
    return render(request, 'epr/career.html', {'published_jobs': published_jobs})

def career_dashboard(request):
    return render(request, 'epr/career_dashboard.html')

def new_post(request):
    return render(request, 'epr/new_post.html')

def create_job_vacancy(request):
    if request.method == 'POST':
        form = JobVacancyForm(request.POST)
        if form.is_valid():
            job = form.save()
            return redirect('epr:job_vacancy_detail', job_id=job.id)  # Redirect to a success page
    else:
        form = JobVacancyForm()
    return render(request, 'epr/job_vacancy_form.html', {'form': form})

def job_vacancy_detail(request, job_id):
    job = get_object_or_404(JobVacancy, id=job_id)
    return render(request, 'epr/job_vacancy_detail.html', {'job': job})

def vacancy_dashboard(request):
    jobs = JobVacancy.objects.all()
    return render(request, 'epr/vacancy_dashboard.html', {'jobs': jobs})

def edit_job_vacancy(request, job_id):
    job = get_object_or_404(JobVacancy, id=job_id)
    if request.method == 'POST':
        form = JobVacancyForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('epr:vacancy_dashboard')
    else:
        form = JobVacancyForm(instance=job)
    return render(request, 'epr/job_vacancy_form.html', {'form': form})

def delete_job_vacancy(request, job_id):
    job = get_object_or_404(JobVacancy, id=job_id)
    job.delete()
    return redirect('epr:vacancy_dashboard')

def publish_job_vacancy(request, job_id):
    job = get_object_or_404(JobVacancy, id=job_id)
    job.published = not job.published  # Toggle publish status
    job.save()
    return redirect('epr:vacancy_dashboard')


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm, RegisterForm, JobVacancyForm, JobApplicationForm, PostForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, BlogPostForm
from django.contrib.auth import login as auth_login, authenticate, get_user_model
from .models import Contact, JobVacancy, JobApplication, Post, Category, BlogPost
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

User = get_user_model()  # This will dynamically use your custom user model


# Create your views here.
def index(request):
    return render(request, 'epr/index.html')

def blog_index(request):
    return render(request, 'blog/index.html')

def blog_detail(request, post_id):  # Change function to accept post_id
    if request.user and not request.user.has_perm('blog.view_post'):
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('epr:blog_index')

    try:
        # Getting data from model by post id
        post = get_object_or_404(Post, id=post_id)  # Change slug to id
        related_posts = Post.objects.filter(category=post.category).exclude(id=post_id)  # Also update this line
    
    except Post.DoesNotExist:
        raise Http404("Post Does not exist")

    return render(request, "blog/detail.html", {'post': post, 'related_posts': related_posts})

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
    other_jobs = JobVacancy.objects.filter(published=True).exclude(id=job.id)  # Fetch other published jobs
    return render(request, 'epr/job_vacancy_detail.html', {'job': job, 'other_jobs': other_jobs})	

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

def apply_job(request, job_id):
    job = get_object_or_404(JobVacancy, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            return redirect('epr:application_success')  # Redirect to a success page
    else:
        form = JobApplicationForm()
    return render(request, 'epr/apply_job.html', {'form': form, 'job': job})

def application_success(request):
    return render(request, 'epr/application_success.html')

def terms_and_conditions(request):
    return render(request, 'epr/terms_and_conditions.html')

def blog_new_post(request):
    form = PostForm()
    categories = Category.objects.all()
    if request.method == "POST":
        #form
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('epr:blog_dashboard')
    return render(request, 'blog/new_post.html', {'categories' : categories, 'form' : form})

def blog_edit_post(request, post_id):
    form = PostForm()
    categories = Category.objects.all()
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        #form
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.save()
            messages.success(request, 'Your post has been updated successfully.')
            return redirect('epr:blog_dashboard')

    return render(request, 'blog/edit_post.html', {'categories' : categories, 'post' : post, 'form' : form})

def blog_dashboard(request):
    blog_title = "My Posts"
    #getting User Posts
    all_posts = Post.objects.filter(user = request.user) 

    #Pagination
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/dashboard.html", {"blogtitle" : blog_title, 'page_object' : page_obj})

def blog_login(request):
    if request.method == "POST":
        #login form
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                print("Login Success!")
                return redirect('blog:dashboard')
            
        else:
            print("Form is not valid")
    else:
        form = LoginForm()
        print("Form is not valid")
    return render(request, "blog/login.html", {"form" : form})

def blog_register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #save data to database
            user.set_password(form.cleaned_data['password'])
            user.save()
            #add user to group
            readers_group, created = Group.objects.get_or_create(name="Readers")
            user.groups.add(readers_group)
            messages.success(request, "Registration successful. You can log in now.")
            return redirect('epr:blog_login')
        else:
            print('Form is not valid')
    return render(request, "blog/register.html", {"form" : form})

def blog_forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == "POST":
        #forgot password form
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            #send email to reset password
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            subject = "Password Reset Request"
            message = render_to_string('blog/reset_password_email.html', {
                'domain': domain,
                'uid' : uid,
                'token' : token
            })
            send_mail(subject, message, 'noreply@kandait.com', [email])
            messages.success(request, 'Email has been sent successfully. Please check your inbox.')
    return render(request, "blog/forgot_password.html", {"form" : form})

def blog_reset_password(request, uidb64, token):
    form = ResetPasswordForm()
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('blog:blog_login')
            else:
                messages.error(request, 'The password reset link is invalid or has expired.')
    return render(request, "blog/reset_password.html", {'form' : form})

def blog_main_dashboard(request):
    posts = Post.objects.filter(is_published=True)  # Fetch only published posts
    return render(request, 'blog/main_dashboard.html', {'posts': posts})

def main_post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'epr/main_post_detail.html', {'post': post})

###################
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('epr:blog_list')  # Redirect to a page showing the list of blog posts
    else:
        form = BlogPostForm()
    return render(request, 'epr/create_blog_post.html', {'form': form})


def blog_list(request):
    # Fetch all blog posts from the database
    posts = BlogPost.objects.all().order_by('-created_at')  # Order by newest first
    return render(request, 'epr/blog_list.html', {'posts': posts})

def blog_detail(request, post_id):
    # Fetch the blog post by ID or return a 404 error if not found
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'epr/blog_detail.html', {'post': post})

def edit_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('epr:blog_list')  # Redirect to the blog list after editing
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'epr/edit_blog_post.html', {'form': form, 'post': post})

def delete_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('epr:blog_list')  # Redirect to the blog list after deleting
    return render(request, 'epr/confirm_delete.html', {'post': post})

def ai_sollution(request):
    return render(request, 'epr/services/AI_Solutions.html')

def digitalMarketing(request):
    return render(request, 'epr/services/digitalMarketing.html')

def IntelligentDataAnalysis(request):
    return render(request, 'epr/services/IntelligentDataAnalysis.html')

def IOTMain(request):
    return render(request, 'epr/services/IOTMain.html')

def mobileMain(request):
    return render(request, 'epr/services/mobileMain.html')

def webMain(request):
    return render(request, 'epr/services/webMain.html')

def about_us(request):
    return render(request, 'epr/about_us.html')
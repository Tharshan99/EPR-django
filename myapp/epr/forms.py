from django import forms
from .models import Contact, JobVacancy, JobApplication, BlogPost
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
from epr.models import Category, Post
User = get_user_model()  # This will dynamically use your custom user model


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'contact', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number', 'type': 'tel'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter your message'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class JobVacancyForm(forms.ModelForm):
    class Meta:
        model = JobVacancy
        fields = ['job_title', 'job_details', 'closing_date', 'qualifications', 'requirements', 'location', 'pay_details', 'job_type']
        widgets = {
            'closing_date': forms.DateInput(attrs={'type': 'date'}),
            'qualifications': forms.Textarea(attrs={'class': 'rich-text-editor'}),
            'requirements': forms.Textarea(attrs={'class': 'rich-text-editor'}),
        }

class JobApplicationForm(forms.ModelForm):
    accept_terms = forms.BooleanField(
        required=True,
        label="I agree to the terms and conditions",
        error_messages={'required': 'You must accept the terms and conditions to proceed.'}
    )

    class Meta:
        model = JobApplication
        fields = ['first_name', 'last_name', 'email', 'confirm_email', 'phone_number', 'place_of_residence', 'message', 'cv']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        phone_number = cleaned_data.get('phone_number')

        # Check if both emails match
        if email and confirm_email and email != confirm_email:
            raise ValidationError("Emails do not match. Please enter the same email in both fields.")

        # Check if phone number has at least 10 digits
        if phone_number and len(phone_number) < 10:
            raise ValidationError("Phone number must have at least 10 digits.")

        # Ensure no field is empty
        for field_name, field_value in cleaned_data.items():
            if not field_value and field_name != 'accept_terms':  # Skip validation for accept_terms
                raise ValidationError(f"{field_name.replace('_', ' ').title()} is required.")

        return cleaned_data
    
class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=200, label='Title', required=True)
    content = forms.CharField(label='Content', required=True)
    category = forms.ModelChoiceField(label='Category', required=True, queryset = Category.objects.all())
    img_url = forms.ImageField(label='Image', required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'img_url']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        

        #custom validation
        if title and len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        
        if content and len(content) < 10:
            raise forms.ValidationError('Content must be at least 10 characters long.')
        
    def save(self, commit=...):
        post = super().save(commit)
        cleaned_data = super().clean()

        if cleaned_data.get('img_url'):
            post.img_url = cleaned_data.get('img_url')
        else:
            img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/450px-No_image_available.svg.png"
            post.img_url = img_url
        
        if commit:
            post.save()
        return post

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username", required=True)
    password = forms.CharField(max_length=100, label="Password", required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            
class RegisterForm(forms.ModelForm) :
    username = forms.CharField(max_length=100, label="Username", required=True)
    email = forms.EmailField(max_length=100, label="Email", required=True)
    password = forms.CharField(max_length=100, label="Password", required=True)
    password_confirm = forms.CharField(max_length=100, label="Confirm Password", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=100, label="Email", required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No User registered with this email")
        
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label="New Password", min_length=8)
    confirm_password = forms.CharField(label="Confirm Password", min_length=8)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        

##############
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        
        if content and len(content) < 10:
            raise forms.ValidationError('Content must be at least 10 characters long.')
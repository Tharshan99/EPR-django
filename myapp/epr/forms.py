from django import forms
from .models import Contact, JobVacancy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
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
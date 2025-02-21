from django.urls import path
from . import views
from .views import create_job_vacancy,vacancy_dashboard

app_name = "epr"

urlpatterns = [
    path('', views.index, name='index'),
    path('post/detail', views.detail, name='detail'),
    path('contact', views.contact, name='contact'),
    path('login109876', views.user_login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('career_dashboard', views.career_dashboard, name='career_dashboard'),	
    path('register', views.register, name='register'),
    path('contact-dashboard', views.contact_dashboard, name='contact_dashboard'),
    path('career', views.career, name='career'),
    path('new_post', views.new_post, name='new_post'),
    path('create/', views.create_job_vacancy, name='create_job_vacancy'),
    path('job/<int:job_id>/', views.job_vacancy_detail, name='job_vacancy_detail'),
    path('vacancy-dashboard', vacancy_dashboard, name='vacancy_dashboard'),
    path('edit/<int:job_id>/', views.edit_job_vacancy, name='edit_job_vacancy'),
    path('delete/<int:job_id>/', views.delete_job_vacancy, name='delete_job_vacancy'),
    path('publish/<int:job_id>/', views.publish_job_vacancy, name='publish_job_vacancy'),
]

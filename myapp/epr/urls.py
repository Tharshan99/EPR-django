from django.urls import path
from . import views
from .views import create_job_vacancy, vacancy_dashboard

app_name = "epr"

urlpatterns = [
    path('', views.index, name='index'),
    # path('post/detail', views.detail, name='detail'),
    path('contact', views.contact, name='contact'),
    path('login109876', views.user_login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    # path('career_dashboard', views.career_dashboard, name='career_dashboard'),	
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
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('application-success/', views.application_success, name='application_success'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    # path('blog_index/', views.blog_index, name='blog_index'),
    # path('blog_detail/<int:post_id>', views.blog_detail, name='blog_detail'),
    # path('blog_new_post/', views.blog_new_post, name='blog_new_post'),
    # path('blog_edit_post/<int:post_id>', views.blog_edit_post, name='blog_edit_post'),
    # path('blog_dashboard/', views.blog_dashboard, name='blog_dashboard'),
    # path('blog_login/', views.blog_login, name='blog_login'),
    # path('blog_register/', views.blog_register, name='blog_register'),
    # path('blog_forgot_password/', views.blog_forgot_password, name='blog_forgot_password'),
    # path('blog_reset_password/<uidb64>/<token>', views.blog_reset_password, name='blog_reset_password'),
    # path('blog_main_dashboard/', views.blog_main_dashboard, name='blog_main_dashboard'),
    # path('post/<int:post_id>/', views.main_post_detail, name='post_detail'),
    # path('blog_create', views.create_blog, name='create_blog'),
    path('blog_list', views.blog_list, name='blog_list'),	
    path('create-blog-post/', views.create_blog_post, name='create_blog_post'),
    path('blog-detail/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('edit-blog-post/<int:post_id>/', views.edit_blog_post, name='edit_blog_post'),
    path('delete-blog-post/<int:post_id>/', views.delete_blog_post, name='delete_blog_post'),
]

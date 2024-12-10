from django.urls import path

from . import views

urlpatterns = [
    path('', views.sign_in_page, name='login'),
    path('sign-out/', views.sign_out_page, name='logout'),
    path('forgot-password/', views.forgot_password_page, name='forgot_password'),
    path('forgot-password/process/', views.process_forgot_password, name='process_forgot_password'),
    path('magic-link/process/', views.process_magic_link, name='process_magic_link'),
    path('verify-email/process/', views.process_verify_email, name='process_verify_email'),
]

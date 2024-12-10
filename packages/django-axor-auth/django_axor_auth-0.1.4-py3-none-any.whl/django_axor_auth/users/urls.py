from django.urls import path, include

from . import views

"""
api/user/
"""
urlpatterns = [
    # Basic
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('delete/', views.delete_user),

    # Get user info
    path('me/', views.me),

    # Verify user
    path('verify_email/resend/', views.resend_verification_email),
    path('verify_email/', views.verify_email),

    # Change stuff
    path('change_password/', views.change_password),
    path('change_name/', views.change_name),
    path('change_email/', views.change_email),

    # Session management
    path('active_sessions/', views.active_sessions),
    path('active_sessions/close/', views.close_session),
    path('active_sessions/close_except_current/', views.close_all_sessions_except_current),

    # Addon modules
    path('totp/', include('django_axor_auth.users.users_totp.urls')),
    path('forgot_password/',
         include('django_axor_auth.users.users_forgot_password.urls')),
    path('magic_link/',
         include('django_axor_auth.users.users_magic_link.urls')),
]

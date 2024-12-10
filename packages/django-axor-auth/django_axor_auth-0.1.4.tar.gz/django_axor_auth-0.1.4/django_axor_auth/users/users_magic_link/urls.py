from django.urls import path
from . import views

"""
/api/user/magic_link/
"""
urlpatterns = [
    path('request/', views.request_magic_link),
    path('consume/', views.consume_magic_link),
]

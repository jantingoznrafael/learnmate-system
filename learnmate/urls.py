"""
URL configuration for learnmate project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('questions.urls')),
    path('notifications/', include('notifications.urls')),
]


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm, CustomAuthenticationForm


def login_view(request):
    """Custom login view with role selection and superuser validation."""
    if request.user.is_authenticated:
        return redirect('questions:home')
    
    error_message = None
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'student')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is trying to login as admin
            if user_type == 'admin':
                # Only allow superusers to login as admin
                if not user.is_superuser:
                    error_message = 'You do not have admin privileges. Please login as a student.'
                    return render(request, 'accounts/login.html', {'error_message': error_message, 'form': form})
            
            login(request, user)
            messages.success(request, 'Login successful!')
            # Redirect admins to admin panel, others to home
            if user_type == 'admin' and user.is_superuser:
                return redirect('admin:index')
            return redirect('questions:home')
        else:
            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                error_message = 'Username does not exist.'
            else:
                error_message = 'Incorrect password.'
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'error_message': error_message, 'form': form})


def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('questions:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to LearnMate.')
            return redirect('questions:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """User profile view."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


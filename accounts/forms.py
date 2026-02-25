from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
import re


class CustomAuthenticationForm(forms.Form):
    """Custom login form with admin/student selection."""
    
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin/Superuser'),
    ]
    
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10',
            'placeholder': 'Username',
            'autofocus': True,
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10',
            'placeholder': 'Password',
        })
    )
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        initial='student',
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        })
    )


class UserRegistrationForm(UserCreationForm):
    """Registration form for new users."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10',
            'placeholder': 'Enter your email address'
        })
    )

    strand = forms.ChoiceField(
        choices=[('', 'Select your strand')] + list(User.STRAND_CHOICES),
        required=True,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10'
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'strand',
            'password1',
            'password2',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10',
                'placeholder': 'Example - RAFAEL.N.TINGZON.240081'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10',
                'placeholder': 'Enter your last name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 resize-y',
                'rows': 3,
                'placeholder': 'Tell us about yourself (optional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10',
            'placeholder': 'Confirm your password'
        })

    def clean_username(self):
        """Validate username format: FIRSTNAME.LASTNAME.IDNUMBER or FIRSTNAME.MIDDLENAME.LASTNAME.IDNUMBER"""
        username = self.cleaned_data.get('username')
        
        if not username:
            raise forms.ValidationError('Username is required.')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username has been used.')
        
        # Check if username is in UPPERCASE
        if username != username.upper():
            raise forms.ValidationError('Username must be in UPPERCASE LETTERS only.')
        
        # Split by dots
        parts = username.split('.')
        
        # Should have 3 parts (FIRSTNAME.LASTNAME.IDNUMBER) or 4 parts (FIRSTNAME.MIDDLENAME.LASTNAME.IDNUMBER)
        if len(parts) not in [3, 4]:
            raise forms.ValidationError(
                'Username format must be either:\n'
                '• FIRSTNAME.LASTNAME.IDNUMBER or\n'
                '• FIRSTNAME.MIDDLENAME.LASTNAME.IDNUMBER'
            )
        
        # Last part should be the ID number (exactly 6 digits)
        id_number = parts[-1]
        if not re.match(r'^\d{6}$', id_number):
            raise forms.ValidationError('ID number must contain exactly 6 digits.')
        
        # All other parts should be letters only
        for i, part in enumerate(parts[:-1]):
            if not part:
                raise forms.ValidationError('Each part of the username must have content.')
            if not re.match(r'^[A-Z]+$', part):
                raise forms.ValidationError('Name parts must contain only UPPERCASE letters.')
        
        return username

    def clean_email(self):
        """Validate that email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email has been used.')
        return email


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'strand']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 bg-slate-50',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 bg-slate-50',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10',
                'placeholder': 'Update your email address'
            }),
            'strand': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border-2 border-slate-300 rounded-xl text-base transition-all focus:outline-none focus:border-primary focus:ring-4 focus:ring-primary/10'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make first & last name read-only
        self.fields['first_name'].widget.attrs['readonly'] = True
        self.fields['last_name'].widget.attrs['readonly'] = True

    # Extra safety: ignore any submitted changes
    def clean_first_name(self):
        return self.instance.first_name

    def clean_last_name(self):
        return self.instance.last_name

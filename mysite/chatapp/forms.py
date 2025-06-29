from allauth.account.forms import ResetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings
import re
import socket

# Try to import dnspython for advanced domain validation
try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False


def validate_email_domain(email):
    """
    Validate if email domain exists and can receive emails
    Uses DNS lookup if dnspython is available, otherwise basic socket check
    """
    domain = email.split('@')[1]
    
    if DNS_AVAILABLE:
        try:
            # Check if MX record exists for the domain
            mx_records = dns.resolver.resolve(domain, 'MX')
            if not mx_records:
                raise ValidationError(f"Domain '{domain}' does not accept emails.")
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, Exception):
            raise ValidationError(f"Domain '{domain}' is not valid or does not exist.")
    else:
        # Fallback: basic domain connectivity check
        try:
            socket.gethostbyname(domain)
        except socket.gaierror:
            raise ValidationError(f"Domain '{domain}' is not valid or does not exist.")
    
    return True


def validate_email_format(email):
    """
    Advanced email format validation
    """
    # Basic Django email validation first
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError("Please enter a valid email address.")
    
    # Additional checks for common invalid patterns
    if '..' in email:
        raise ValidationError("Email cannot contain consecutive dots.")
    
    if email.startswith('.') or email.endswith('.'):
        raise ValidationError("Email cannot start or end with a dot.")
    
    # Check for valid characters
    local_part, domain = email.rsplit('@', 1)
    
    # Local part validation
    if len(local_part) > 64:
        raise ValidationError("Email address is too long.")
    
    # Domain validation
    if len(domain) > 255:
        raise ValidationError("Email domain is too long.")
    
    return True


class CustomRegistrationForm(forms.Form):
    """
    Custom registration form with comprehensive email validation
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white',
            'placeholder': 'Enter username'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white',
            'placeholder': 'Enter your email address'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white',
            'placeholder': 'Enter password'
        })
    )
    
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white',
            'placeholder': 'Confirm password'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if not username:
            raise ValidationError("Username is required.")
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
        
        # Username validation
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        
        # Check for valid characters (alphanumeric and underscore only)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not email:
            raise ValidationError("Email address is required.")
        
        # Format validation
        validate_email_format(email)
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email address already exists.")
        
        # Domain validation (optional - can be disabled for faster registration)
        try:
            validate_email_domain(email)
        except ValidationError as e:
            # For production, you might want to log this and allow registration anyway
            # For now, we'll enforce domain validation
            raise e
        
        return email.lower()  # Store email in lowercase
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if not password:
            raise ValidationError("Password is required.")
        
        # Password strength validation
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        # Check for at least one number
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one number.")
        
        # Check for at least one letter
        if not re.search(r'[a-zA-Z]', password):
            raise ValidationError("Password must contain at least one letter.")
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise ValidationError("Passwords do not match.")
        
        return cleaned_data
    
    def save(self):
        """
        Create and return a new user
        """
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return user


class CustomResetPasswordForm(ResetPasswordForm):
    """
    Custom password reset form that checks if email exists before sending reset email
    """
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if user with this email exists
        if not User.objects.filter(email=email).exists():
            raise ValidationError(
                "This email address is not associated with any account. "
                "Please check your email or register for a new account."
            )
        
        return email
    
    def save(self, request, **kwargs):
        """
        Only send email if user exists (validation already passed)
        """
        email = self.cleaned_data["email"]
        
        # Get the users for this email (should exist since we validated above)
        self.users = User.objects.filter(email=email)
        
        if not self.users.exists():
            # This shouldn't happen due to clean_email validation, but just in case
            raise ValidationError(
                "This email address is not associated with any account."
            )
        
        return super().save(request, **kwargs)

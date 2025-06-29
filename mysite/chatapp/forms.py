from allauth.account.forms import ResetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


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

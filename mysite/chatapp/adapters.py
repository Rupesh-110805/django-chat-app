from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from .models import UserBlock
import logging

logger = logging.getLogger(__name__)

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        """
        logger.info(f"Pre-social login: {sociallogin.user.email}")
        
        # Check if user is blocked (for existing users)
        if sociallogin.user.pk:  # User already exists
            block = UserBlock.is_user_blocked(sociallogin.user)
            if block:
                logger.warning(f"Blocked user {sociallogin.user.username} attempted Google login")
                messages.error(request, f"Your account has been blocked. Reason: {block.reason}")
                # Prevent login by raising an exception or setting user to None
                sociallogin.user = None
                return
    
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login. In case of auto-signup,
        this will be called on a POST request.
        """
        user = super().save_user(request, sociallogin, form)
        logger.info(f"Saved user: {user.username} ({user.email})")
        return user
        
    def populate_user(self, request, sociallogin, data):
        """
        Populates user information from social provider info.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Ensure the user has required fields
        if not user.first_name and 'given_name' in data:
            user.first_name = data.get('given_name', '')
        if not user.last_name and 'family_name' in data:
            user.last_name = data.get('family_name', '')
        if not user.username:
            # Create username from email if not provided
            user.username = user.email.split('@')[0]
            
        logger.info(f"Populated user: {user.username} ({user.email})")
        return user

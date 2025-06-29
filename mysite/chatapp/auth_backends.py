from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserBlock
import logging

logger = logging.getLogger(__name__)

class BlockAwareAuthenticationBackend(ModelBackend):
    """
    Custom authentication backend that checks if user is blocked
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        # First, do normal authentication
        user = super().authenticate(request, username, password, **kwargs)
        
        if user:
            # Check if user is blocked
            block = UserBlock.is_user_blocked(user)
            if block:
                logger.warning(f"Blocked user {user.username} attempted to login")
                return None  # Prevent login
                
        return user
    
    def user_can_authenticate(self, user):
        """
        Check if user can authenticate (not blocked)
        """
        if not super().user_can_authenticate(user):
            return False
            
        # Check if user is blocked
        block = UserBlock.is_user_blocked(user)
        if block:
            return False
            
        return True

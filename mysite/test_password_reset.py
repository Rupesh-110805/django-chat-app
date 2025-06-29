#!/usr/bin/env python
"""
Test script to verify password reset functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.utils import override_settings

@override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1'])
def test_password_reset():
    client = Client()
    
    print("=== Testing Password Reset Functionality ===\n")
    
    # Test 1: Non-existent email
    print("1. Testing with non-existent email...")
    response = client.post(reverse('account_reset_password'), {
        'email': 'nonexistent@example.com'
    })
    
    if response.status_code == 200:
        # Check if form has errors
        if hasattr(response, 'context') and response.context and 'form' in response.context and response.context['form'].errors:
            print("✅ SUCCESS: Form validation failed for non-existent email")
            print(f"   Error: {response.context['form'].errors['email'][0]}")
        else:
            print("❌ FAILURE: No form errors found for non-existent email")
            print(f"   Content preview: {response.content.decode()[:200]}...")
    else:
        print(f"❌ FAILURE: Unexpected status code: {response.status_code}")
    
    print()
    
    # Test 2: Existing email
    print("2. Testing with existing email...")
    existing_user = User.objects.first()
    if existing_user and existing_user.email:
        response = client.post(reverse('account_reset_password'), {
            'email': existing_user.email
        })
        
        if response.status_code == 302:  # Redirect to success page
            print("✅ SUCCESS: Password reset initiated for existing user")
            print(f"   Email: {existing_user.email}")
        elif response.status_code == 200:
            if hasattr(response, 'context') and response.context and 'form' in response.context and response.context['form'].errors:
                print("❌ FAILURE: Form validation failed for existing email")
                print(f"   Error: {response.context['form'].errors}")
            else:
                print("✅ SUCCESS: Form processed without errors")
        else:
            print(f"❌ FAILURE: Unexpected status code: {response.status_code}")
    else:
        print("❌ FAILURE: No users with email found")
    
    print()
    
    # Test 3: Empty email
    print("3. Testing with empty email...")
    response = client.post(reverse('account_reset_password'), {
        'email': ''
    })
    
    if response.status_code == 200:
        if hasattr(response, 'context') and response.context and 'form' in response.context and response.context['form'].errors:
            print("✅ SUCCESS: Form validation failed for empty email")
            print(f"   Error: {response.context['form'].errors}")
        else:
            print("❌ FAILURE: No form errors found for empty email")
    else:
        print(f"❌ FAILURE: Unexpected status code: {response.status_code}")

if __name__ == '__main__':
    test_password_reset()

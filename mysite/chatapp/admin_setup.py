from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def setup_admin(request):
    """
    Emergency admin setup view - only works if no superusers exist
    Access at: /setup-admin/
    """
    # Check if any superusers exist
    if User.objects.filter(is_superuser=True).exists():
        existing_superusers = User.objects.filter(is_superuser=True)
        superuser_info = []
        for su in existing_superusers:
            superuser_info.append(f"Username: {su.username}, Email: {su.email}")
        
        return HttpResponse(f"""
        <h2>Superusers Already Exist</h2>
        <p>The following superusers are already created:</p>
        <ul>
        {''.join([f'<li>{info}</li>' for info in superuser_info])}
        </ul>
        <p><strong>Try these login credentials:</strong></p>
        <ul>
        <li>Your environment variables: admin / rupesh</li>
        <li>Backup account: chatadmin / ChatApp2025!</li>
        </ul>
        <p><a href="/admin/">Go to Admin Panel</a></p>
        <p><a href="/">Back to Chat App</a></p>
        """)
    
    if request.method == 'POST':
        try:
            # Create emergency superuser
            emergency_user = User.objects.create_superuser(
                username='emergency',
                email='emergency@chatapp.com',
                password='Emergency123!'
            )
            return HttpResponse(f"""
            <h2>Emergency Superuser Created!</h2>
            <p><strong>Username:</strong> emergency</p>
            <p><strong>Password:</strong> Emergency123!</p>
            <p><strong>Email:</strong> emergency@chatapp.com</p>
            <p><a href="/admin/">Go to Admin Panel</a></p>
            <p><a href="/">Back to Chat App</a></p>
            """)
        except Exception as e:
            return HttpResponse(f"""
            <h2>Error Creating Superuser</h2>
            <p>Error: {e}</p>
            <p><a href="/">Back to Chat App</a></p>
            """)
    
    return HttpResponse("""
    <h2>Emergency Admin Setup</h2>
    <p>No superusers found. Click the button below to create an emergency admin account.</p>
    <form method="post">
        <button type="submit" style="padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px;">
            Create Emergency Admin
        </button>
    </form>
    <p><a href="/">Back to Chat App</a></p>
    """)

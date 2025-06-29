from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings

@staff_member_required
def setup_google_oauth(request):
    """Setup Google OAuth2 social application"""
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        client_secret = request.POST.get('client_secret')
        
        if not client_id or not client_secret:
            messages.error(request, 'Both Client ID and Client Secret are required.')
            return render(request, 'chatapp/setup_google_oauth.html')
        
        # Get or create the default site
        site = Site.objects.get(pk=1)
        
        # Create or update Google social app
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': client_id,
                'secret': client_secret,
            }
        )
        
        if not created:
            google_app.client_id = client_id
            google_app.secret = client_secret
            google_app.save()
        
        # Add the site to the app
        google_app.sites.add(site)
        
        action = 'created' if created else 'updated'
        messages.success(request, f'Google OAuth2 application has been {action} successfully!')
        return redirect('index')
    
    return render(request, 'chatapp/setup_google_oauth.html')

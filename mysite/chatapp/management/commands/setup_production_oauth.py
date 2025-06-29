from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Setup production site and social application for Google OAuth'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='django-chat-app-nhzc.onrender.com',
            help='Production domain name'
        )
        parser.add_argument(
            '--client-id',
            type=str,
            default='928381654908-n6p7upjh9lslsm1ef0ai5rmgs2qp0kq7.apps.googleusercontent.com',
            help='Google OAuth Client ID'
        )
        parser.add_argument(
            '--client-secret',
            type=str,
            default='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',
            help='Google OAuth Client Secret'
        )

    def handle(self, *args, **options):
        domain = options['domain']
        client_id = options['client_id']
        client_secret = options['client_secret']

        self.stdout.write(f"🚀 Setting up production OAuth for: {domain}")

        # Update the default site
        try:
            site = Site.objects.get(id=1)
            site.domain = domain
            site.name = 'Django Chat App'
            site.save()
            self.stdout.write(
                self.style.SUCCESS(f"✅ Updated site domain to: {domain}")
            )
        except Site.DoesNotExist:
            site = Site.objects.create(
                id=1,
                domain=domain,
                name='Django Chat App'
            )
            self.stdout.write(
                self.style.SUCCESS(f"✅ Created new site: {domain}")
            )

        # Create or update Google Social Application
        try:
            social_app = SocialApp.objects.get(provider='google')
            social_app.name = 'Google OAuth'
            social_app.client_id = client_id
            social_app.secret = client_secret
            social_app.save()
            
            # Ensure the site is associated
            if site not in social_app.sites.all():
                social_app.sites.add(site)
            
            self.stdout.write(
                self.style.SUCCESS("✅ Updated existing Google Social Application")
            )
        except SocialApp.DoesNotExist:
            social_app = SocialApp.objects.create(
                provider='google',
                name='Google OAuth',
                client_id=client_id,
                secret=client_secret
            )
            social_app.sites.add(site)
            self.stdout.write(
                self.style.SUCCESS("✅ Created new Google Social Application")
            )

        self.stdout.write("\n🎉 Production OAuth setup complete!")
        self.stdout.write("\nNext steps:")
        self.stdout.write("1. Update Google Cloud Console with these URIs:")
        self.stdout.write(f"   - JavaScript origin: https://{domain}")
        self.stdout.write(f"   - Redirect URI: https://{domain}/accounts/google/login/callback/")
        self.stdout.write("2. Test Google login on your production site")
        self.stdout.write(f"3. Visit: https://{domain}/accounts/login/")

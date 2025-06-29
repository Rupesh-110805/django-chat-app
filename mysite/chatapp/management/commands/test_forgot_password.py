from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    help = 'Test the complete forgot password flow'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email address to test with', required=True)
        parser.add_argument('--create-user', action='store_true', help='Create test user if not exists')

    def handle(self, *args, **options):
        email = options['email']
        
        # Check if user exists or create one
        try:
            user = User.objects.get(email=email)
            self.stdout.write(f'Found existing user: {user.username} ({user.email})')
        except User.DoesNotExist:
            if options['create_user']:
                username = email.split('@')[0]
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='testpassword123'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created test user: {user.username} ({user.email})')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'User with email {email} not found. Use --create-user to create one.')
                )
                return

        # Create email address record for allauth
        email_address, created = EmailAddress.objects.get_or_create(
            user=user,
            email=email,
            defaults={'verified': True, 'primary': True}
        )
        
        if created:
            self.stdout.write(f'Created EmailAddress record for {email}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Test Setup Complete!'))
        self.stdout.write('')
        self.stdout.write('🔗 Now test the password reset flow:')
        self.stdout.write('1. Go to: http://127.0.0.1:8000/accounts/login/')
        self.stdout.write('2. Click "Forgot your password?"')
        self.stdout.write(f'3. Enter email: {email}')
        self.stdout.write('4. Check terminal for reset email')
        self.stdout.write('5. Copy the reset URL and test it')
        self.stdout.write('')
        self.stdout.write(f'Test User Credentials:')
        self.stdout.write(f'  Username: {user.username}')
        self.stdout.write(f'  Email: {user.email}')
        self.stdout.write(f'  Password: testpassword123')

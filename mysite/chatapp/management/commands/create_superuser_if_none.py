"""
Management command to create a superuser automatically if one doesn't exist.
This is useful for deployment where we can't run interactive commands.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser if one does not exist'

    def handle(self, *args, **options):
        # Get superuser credentials from environment variables with better defaults
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@chatapp.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123!')

        # Check if any superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS('Superuser already exists.')
            )
            return

        # Create superuser
        try:
            superuser = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser "{username}" created successfully with email "{email}"'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    f'Default password is: {password}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'Please change the password after first login!'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
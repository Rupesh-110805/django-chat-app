from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from chatapp.models import UserBlock


class Command(BaseCommand):
    help = 'Test user blocking functionality'

    def add_arguments(self, parser):
        parser.add_argument('--create-test-users', action='store_true', help='Create test users for blocking tests')
        parser.add_argument('--block-user', type=str, help='Block a user by username')
        parser.add_argument('--unblock-user', type=str, help='Unblock a user by username')
        parser.add_argument('--list-blocks', action='store_true', help='List all current blocks')

    def handle(self, *args, **options):
        if options['create_test_users']:
            self.create_test_users()
        elif options['block_user']:
            self.block_user(options['block_user'])
        elif options['unblock_user']:
            self.unblock_user(options['unblock_user'])
        elif options['list_blocks']:
            self.list_blocks()
        else:
            self.stdout.write(self.style.ERROR('Please specify an action'))

    def create_test_users(self):
        """Create some test users for blocking functionality"""
        test_users = [
            {'username': 'testuser1', 'email': 'test1@example.com', 'first_name': 'Test', 'last_name': 'User One'},
            {'username': 'testuser2', 'email': 'test2@example.com', 'first_name': 'Test', 'last_name': 'User Two'},
            {'username': 'testuser3', 'email': 'test3@example.com', 'first_name': 'Test', 'last_name': 'User Three'},
        ]
        
        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created test user: {user.username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User {user.username} already exists')
                )

    def block_user(self, username):
        """Block a user temporarily"""
        try:
            user = User.objects.get(username=username)
            admin_user = User.objects.filter(is_superuser=True).first()
            
            if not admin_user:
                self.stdout.write(self.style.ERROR('No admin user found to perform the block'))
                return
            
            # Remove existing blocks
            UserBlock.objects.filter(user=user, is_active=True).update(is_active=False)
            
            # Create new block (1 day for testing)
            block = UserBlock.objects.create(
                user=user,
                blocked_by=admin_user,
                reason='Test block via management command',
                block_type='temporary',
                blocked_until=timezone.now() + timezone.timedelta(days=1)
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Blocked user {username} until {block.blocked_until}')
            )
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} not found'))

    def unblock_user(self, username):
        """Unblock a user"""
        try:
            user = User.objects.get(username=username)
            updated_count = UserBlock.objects.filter(user=user, is_active=True).update(is_active=False)
            
            if updated_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'Unblocked user {username} (deactivated {updated_count} block(s))')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User {username} was not blocked')
                )
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} not found'))

    def list_blocks(self):
        """List all current blocks"""
        active_blocks = UserBlock.objects.filter(
            is_active=True
        ).filter(
            models.Q(block_type='permanent') | models.Q(blocked_until__gt=timezone.now())
        ).select_related('user', 'blocked_by')
        
        if not active_blocks.exists():
            self.stdout.write(self.style.SUCCESS('No active blocks found'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Found {active_blocks.count()} active block(s):'))
        self.stdout.write('')
        
        for block in active_blocks:
            status = 'PERMANENT' if block.block_type == 'permanent' else f'Until {block.blocked_until}'
            self.stdout.write(f'  User: {block.user.username}')
            self.stdout.write(f'  Email: {block.user.email}')
            self.stdout.write(f'  Reason: {block.reason}')
            self.stdout.write(f'  Blocked by: {block.blocked_by.username}')
            self.stdout.write(f'  Status: {status}')
            self.stdout.write(f'  Created: {block.blocked_at}')
            self.stdout.write('  ' + '-' * 40)

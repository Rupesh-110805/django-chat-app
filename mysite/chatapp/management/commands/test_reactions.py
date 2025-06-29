from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chatapp.models import ChatRoom, ChatMessage, MessageReaction

class Command(BaseCommand):
    help = 'Create test messages and reactions'

    def handle(self, *args, **options):
        # Get or create a test room
        room, created = ChatRoom.objects.get_or_create(
            slug='test-room',
            defaults={'name': 'Test Room'}
        )
        
        # Get admin user
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin user not found. Please create a superuser first.'))
            return
        
        # Create a test message
        message = ChatMessage.objects.create(
            user=admin_user,
            room=room,
            message_content="Hello! This is a test message for emoji reactions 🎉",
            message_type='text'
        )
        
        # Add some test reactions
        MessageReaction.objects.create(
            message=message,
            user=admin_user,
            emoji='👍'
        )
        
        MessageReaction.objects.create(
            message=message,
            user=admin_user,
            emoji='❤️'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created test message with reactions in room: {room.name}')
        )
        self.stdout.write(f'Message ID: {message.id}')
        self.stdout.write(f'Room URL: http://127.0.0.1:8000/{room.slug}/')

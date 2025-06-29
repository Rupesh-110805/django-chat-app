from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
import secrets
import string

# Create your models here.

class UserBlock(models.Model):
    """Model to manage user blocking by admins"""
    BLOCK_TYPES = (
        ('temporary', 'Temporary'),
        ('permanent', 'Permanent'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocks')
    blocked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')
    block_type = models.CharField(max_length=10, choices=BLOCK_TYPES, default='temporary')
    reason = models.TextField(help_text="Reason for blocking this user")
    blocked_at = models.DateTimeField(auto_now_add=True)
    blocked_until = models.DateTimeField(null=True, blank=True, help_text="Leave empty for permanent block")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-blocked_at',)
    
    def __str__(self):
        if self.block_type == 'permanent':
            return f'{self.user.username} - Permanently blocked by {self.blocked_by.username}'
        return f'{self.user.username} - Blocked until {self.blocked_until} by {self.blocked_by.username}'
    
    @property
    def is_currently_blocked(self):
        """Check if the block is currently active"""
        if not self.is_active:
            return False
        if self.block_type == 'permanent':
            return True
        return self.blocked_until and timezone.now() < self.blocked_until
    
    @classmethod
    def is_user_blocked(cls, user):
        """Check if a user is currently blocked"""
        active_blocks = cls.objects.filter(
            user=user,
            is_active=True
        )
        
        for block in active_blocks:
            if block.is_currently_blocked:
                return block
        return None
    
    @classmethod
    def unblock_expired_users(cls):
        """Automatically unblock users whose temporary blocks have expired"""
        expired_blocks = cls.objects.filter(
            block_type='temporary',
            is_active=True,
            blocked_until__lte=timezone.now()
        )
        expired_blocks.update(is_active=False)
        return expired_blocks.count()

class ChatRoom(models.Model):
    ROOM_TYPES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='public')
    access_code = models.CharField(max_length=20, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({'Private' if self.room_type == 'private' else 'Public'})"
    
    def save(self, *args, **kwargs):
        # Generate access code for private rooms
        if self.room_type == 'private' and not self.access_code:
            self.access_code = self.generate_access_code()
        elif self.room_type == 'public':
            self.access_code = None
        super().save(*args, **kwargs)
    
    def generate_access_code(self):
        """Generate a unique 8-character access code for private rooms"""
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))


class PrivateRoomMembership(models.Model):
    """Model to track which users have joined private rooms"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'room')
    
    def __str__(self):
        return f'{self.user.username} joined {self.room.name}'


class UserPresence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('user', 'room')
    
    def __str__(self):
        return f'{self.user.username} in {self.room.name} - {"Online" if self.is_online else "Offline"}'
    
    @classmethod
    def update_user_presence(cls, user, room):
        """Update or create user presence in a room"""
        presence, created = cls.objects.get_or_create(
            user=user, 
            room=room,
            defaults={'is_online': True}
        )
        if not created:
            presence.is_online = True
            presence.save()
        return presence
    
    @classmethod
    def set_user_offline(cls, user, room):
        """Set user offline in a room"""
        try:
            presence = cls.objects.get(user=user, room=room)
            presence.is_online = False
            presence.save()
        except cls.DoesNotExist:
            pass
    
    @classmethod
    def get_online_users(cls, room):
        """Get all online users in a room"""
        # Consider users offline if they haven't been seen for more than 5 minutes
        cutoff_time = timezone.now() - timezone.timedelta(minutes=5)
        return cls.objects.filter(
            room=room,
            is_online=True,
            last_seen__gte=cutoff_time
        ).select_related('user')

def upload_to_chat_files(instance, filename):
    return f'chat_files/{instance.room.slug}/{filename}'

class ChatMessage(models.Model):
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('file', 'File'),
        ('image', 'Image'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message_content = models.TextField(blank=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    file = models.FileField(upload_to=upload_to_chat_files, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('date',)
    
    def __str__(self):
        if self.message_type == 'text':
            return f'{self.user.username}: {self.message_content[:50]}'
        else:
            return f'{self.user.username}: [{self.message_type}] {self.file_name}'
    
    def get_file_extension(self):
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return ''
    
    def is_image(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        return self.get_file_extension() in image_extensions
    
    def get_file_size_display(self):
        if self.file_size == 0:
            return ''
        if self.file_size < 1024:
            return f'{self.file_size} B'
        elif self.file_size < 1024 * 1024:
            return f'{self.file_size // 1024} KB'
        else:
            return f'{self.file_size // (1024 * 1024)} MB'

class MessageReaction(models.Model):
    """Model to store emoji reactions to messages"""
    EMOJI_CHOICES = [
        ('👍', 'Thumbs Up'),
        ('👎', 'Thumbs Down'),
        ('❤️', 'Heart'),
        ('😂', 'Laughing'),
        ('😮', 'Wow'),
        ('😢', 'Sad'),
        ('😡', 'Angry'),
        ('🎉', 'Party'),
        ('🔥', 'Fire'),
        ('💯', 'Hundred'),
    ]
    
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10, choices=EMOJI_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('message', 'user', 'emoji')
        ordering = ('created_at',)
    
    def __str__(self):
        return f'{self.user.username} reacted {self.emoji} to message {self.message.id}'
    
    @classmethod
    def toggle_reaction(cls, message, user, emoji):
        """Toggle a reaction - add if doesn't exist, remove if exists"""
        reaction, created = cls.objects.get_or_create(
            message=message,
            user=user,
            emoji=emoji
        )
        if not created:
            reaction.delete()
            return None
        return reaction

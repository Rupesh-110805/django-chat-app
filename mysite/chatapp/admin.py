from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.contrib import messages
from django.utils.html import format_html
from .models import ChatRoom, ChatMessage, MessageReaction, UserPresence, UserBlock


# User Block Admin
@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):
    list_display = ('user', 'blocked_by', 'reason', 'block_type', 'blocked_until', 'blocked_at', 'is_currently_blocked')
    list_filter = ('block_type', 'blocked_at', 'blocked_until', 'is_active')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'reason')
    readonly_fields = ('blocked_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'blocked_by')
        }),
        ('Block Details', {
            'fields': ('reason', 'block_type', 'blocked_until', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('blocked_at',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['unblock_users', 'extend_block_1_day', 'extend_block_1_week', 'make_permanent']
    
    def is_currently_blocked(self, obj):
        """Check if the block is currently active"""
        return obj.is_currently_blocked
    is_currently_blocked.boolean = True
    is_currently_blocked.short_description = 'Currently Blocked'
    
    def unblock_users(self, request, queryset):
        """Custom action to unblock selected users"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'Successfully unblocked {count} user(s).', messages.SUCCESS)
    unblock_users.short_description = "Unblock selected users"
    
    def extend_block_1_day(self, request, queryset):
        """Extend block by 1 day"""
        count = 0
        for block in queryset:
            if block.block_type == 'temporary':
                if block.blocked_until:
                    block.blocked_until += timezone.timedelta(days=1)
                else:
                    block.blocked_until = timezone.now() + timezone.timedelta(days=1)
                block.save()
                count += 1
        self.message_user(request, f'Extended block by 1 day for {count} user(s).', messages.SUCCESS)
    extend_block_1_day.short_description = "Extend block by 1 day"
    
    def extend_block_1_week(self, request, queryset):
        """Extend block by 1 week"""
        count = 0
        for block in queryset:
            if block.block_type == 'temporary':
                if block.blocked_until:
                    block.blocked_until += timezone.timedelta(weeks=1)
                else:
                    block.blocked_until = timezone.now() + timezone.timedelta(weeks=1)
                block.save()
                count += 1
        self.message_user(request, f'Extended block by 1 week for {count} user(s).', messages.SUCCESS)
    extend_block_1_week.short_description = "Extend block by 1 week"
    
    def make_permanent(self, request, queryset):
        """Make blocks permanent"""
        count = queryset.update(block_type='permanent', blocked_until=None)
        self.message_user(request, f'Made {count} block(s) permanent.', messages.SUCCESS)
    make_permanent.short_description = "Make blocks permanent"


# Enhanced User Admin with blocking capabilities
class UserBlockInline(admin.TabularInline):
    model = UserBlock
    fk_name = 'user'  # Specify which ForeignKey to use
    extra = 0
    readonly_fields = ('blocked_at',)
    fields = ('blocked_by', 'reason', 'block_type', 'blocked_until', 'is_active', 'blocked_at')


class CustomUserAdmin(UserAdmin):
    """Extended UserAdmin with blocking capabilities"""
    
    # Add our custom fields to the list display
    list_display = UserAdmin.list_display + ('is_blocked', 'last_login')
    
    # Add our inline for user blocks
    inlines = [UserBlockInline]
    
    # Add our custom actions
    actions = ['block_user_1_day', 'block_user_1_week', 'block_user_permanent', 'unblock_user']
    
    def is_blocked(self, obj):
        """Check if user is currently blocked"""
        return UserBlock.is_user_blocked(obj) is not None
    is_blocked.boolean = True
    is_blocked.short_description = 'Currently Blocked'
    
    def block_user_1_day(self, request, queryset):
        """Block selected users for 1 day"""
        count = 0
        for user in queryset:
            if user.is_superuser:
                continue  # Don't block superusers
            # Deactivate existing blocks for this user
            UserBlock.objects.filter(user=user, is_active=True).update(is_active=False)
            # Create new block
            UserBlock.objects.create(
                user=user,
                blocked_by=request.user,
                reason="Blocked via admin action (1 day)",
                block_type='temporary',
                blocked_until=timezone.now() + timezone.timedelta(days=1)
            )
            count += 1
        self.message_user(request, f'Blocked {count} user(s) for 1 day.', messages.SUCCESS)
    block_user_1_day.short_description = "Block for 1 day"
    
    def block_user_1_week(self, request, queryset):
        """Block selected users for 1 week"""
        count = 0
        for user in queryset:
            if user.is_superuser:
                continue  # Don't block superusers
            # Deactivate existing blocks for this user
            UserBlock.objects.filter(user=user, is_active=True).update(is_active=False)
            # Create new block
            UserBlock.objects.create(
                user=user,
                blocked_by=request.user,
                reason="Blocked via admin action (1 week)",
                block_type='temporary',
                blocked_until=timezone.now() + timezone.timedelta(weeks=1)
            )
            count += 1
        self.message_user(request, f'Blocked {count} user(s) for 1 week.', messages.SUCCESS)
    block_user_1_week.short_description = "Block for 1 week"
    
    def block_user_permanent(self, request, queryset):
        """Block selected users permanently"""
        count = 0
        for user in queryset:
            if user.is_superuser:
                continue  # Don't block superusers
            # Deactivate existing blocks for this user
            UserBlock.objects.filter(user=user, is_active=True).update(is_active=False)
            # Create new permanent block
            UserBlock.objects.create(
                user=user,
                blocked_by=request.user,
                reason="Permanently blocked via admin action",
                block_type='permanent'
            )
            count += 1
        self.message_user(request, f'Permanently blocked {count} user(s).', messages.SUCCESS)
    block_user_permanent.short_description = "Block permanently"
    
    def unblock_user(self, request, queryset):
        """Unblock selected users"""
        count = 0
        for user in queryset:
            updated_count = UserBlock.objects.filter(user=user, is_active=True).update(is_active=False)
            if updated_count > 0:
                count += 1
        self.message_user(request, f'Unblocked {count} user(s).', messages.SUCCESS)
    unblock_user.short_description = "Unblock users"


# Replace the default User admin with our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register existing models
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(MessageReaction)
admin.site.register(UserPresence)

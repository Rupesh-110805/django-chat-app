# Generated by Django 5.1.1 on 2025-06-28 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


def set_default_values(apps, schema_editor):
    """Set default values for existing ChatRoom records"""
    ChatRoom = apps.get_model('chatapp', 'ChatRoom')
    User = apps.get_model('auth', 'User')
    
    # Get the first user as default owner, or create a system user
    try:
        default_user = User.objects.first()
        if not default_user:
            # Create a system user if no users exist
            default_user = User.objects.create_user(
                username='system',
                email='system@example.com',
                password='systempassword'
            )
    except Exception:
        # Fallback - will be handled by Django
        pass
    
    # Update existing rooms to be public and set owner
    for room in ChatRoom.objects.all():
        room.room_type = 'public'
        room.owner_id = default_user.id if default_user else 1
        room.created_at = django.utils.timezone.now()
        room.save()


def reverse_default_values(apps, schema_editor):
    """Reverse migration - remove the fields"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatapp', '0005_messagereaction'),
    ]

    operations = [
        # First add the fields with null=True to allow existing records
        migrations.AddField(
            model_name='chatroom',
            name='room_type',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=10),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='access_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owned_rooms', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatroom',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        
        # Create the PrivateRoomMembership model
        migrations.CreateModel(
            name='PrivateRoomMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatapp.chatroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'room')},
            },
        ),
        
        # Run the data migration to set default values
        migrations.RunPython(set_default_values, reverse_default_values),
    ]

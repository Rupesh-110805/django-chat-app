from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ChatRoom, ChatMessage, UserPresence, MessageReaction, PrivateRoomMembership, UserBlock
from .forms import CustomRegistrationForm

# Create your views here.
def index(request):
    # Only show public rooms on the main page
    chatrooms = ChatRoom.objects.filter(room_type='public').order_by('-created_at')
    return render(request, 'chatapp/index.html', {'chatrooms': chatrooms})

@login_required
def chatroom(request, slug):
    chatroom = get_object_or_404(ChatRoom, slug=slug)
    
    # Check if user has access to private room
    if chatroom.room_type == 'private':
        # Room owner always has access
        if chatroom.owner != request.user:
            # Check if user is a member of the private room
            if not PrivateRoomMembership.objects.filter(user=request.user, room=chatroom).exists():
                messages.error(request, 'You do not have access to this private room.')
                return redirect('private_rooms')
    
    # Update user presence when entering room
    UserPresence.update_user_presence(request.user, chatroom)
    
    # Get the last 30 messages for initial display
    all_messages = ChatMessage.objects.filter(room=chatroom).order_by('date').prefetch_related('reactions__user')
    chat_messages = all_messages[max(0, all_messages.count() - 30):]
    
    # Prepare reaction data for each message
    for message in chat_messages:
        reaction_counts = {}
        for reaction in message.reactions.all():
            emoji_key = reaction.emoji
            if emoji_key not in reaction_counts:
                reaction_counts[emoji_key] = {
                    'count': 0,
                    'users': [],
                    'user_reacted': False
                }
            reaction_counts[emoji_key]['count'] += 1
            reaction_counts[emoji_key]['users'].append(reaction.user.username)
            if reaction.user == request.user:
                reaction_counts[emoji_key]['user_reacted'] = True
        
        message.reaction_data = reaction_counts
    
    # Get online users
    online_users = UserPresence.get_online_users(chatroom)
    
    return render(request, 'chatapp/room.html', {
        'chatroom': chatroom, 
        'chat_messages': chat_messages,
        'online_users': online_users
    })

@login_required
def update_presence(request, slug):
    """Update user presence via AJAX"""
    try:
        chatroom = ChatRoom.objects.get(slug=slug)
        UserPresence.update_user_presence(request.user, chatroom)
        
        # Get updated online users list
        online_users = UserPresence.get_online_users(chatroom)
        users_data = []
        for presence in online_users:
            users_data.append({
                'username': presence.user.username,
                'last_seen': presence.last_seen.strftime('%H:%M'),
                'is_current_user': presence.user == request.user
            })
        
        return JsonResponse({'success': True, 'online_users': users_data})
    except ChatRoom.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Room not found'})

@login_required
def leave_room(request, slug):
    """Set user offline when leaving room"""
    try:
        chatroom = ChatRoom.objects.get(slug=slug)
        UserPresence.set_user_offline(request.user, chatroom)
        return JsonResponse({'success': True})
    except ChatRoom.DoesNotExist:
        return JsonResponse({'success': False})

@login_required
@require_POST
def send_message(request, slug):
    """Send a message to a chat room"""
    if request.method == 'POST':
        room = get_object_or_404(ChatRoom, slug=slug)
        message = request.POST.get('message', '').strip()
        
        if message:
            chat_message = ChatMessage.objects.create(
                user=request.user,
                room=room,
                message=message
            )
            return JsonResponse({'status': 'success', 'message_id': chat_message.id})
    
    return JsonResponse({'status': 'error'})

@login_required
def get_messages(request, slug):
    """Get messages for a chat room"""
    room = get_object_or_404(ChatRoom, slug=slug)
    messages = ChatMessage.objects.filter(room=room).order_by('-date')[:50]
    
    messages_data = []
    for msg in messages:
        messages_data.append({
            'id': msg.id,
            'user': msg.user.username,
            'message': msg.message,
            'date': msg.date.isoformat(),
        })
    
    return JsonResponse({'messages': messages_data})

@login_required
def toggle_reaction(request, slug, message_id):
    """Toggle reaction on a message"""
    if request.method == 'POST':
        room = get_object_or_404(ChatRoom, slug=slug)
        message = get_object_or_404(ChatMessage, id=message_id, room=room)
        emoji = request.POST.get('emoji')
        
        if emoji:
            reaction, created = MessageReaction.objects.get_or_create(
                user=request.user,
                message=message,
                emoji=emoji
            )
            
            if not created:
                reaction.delete()
                return JsonResponse({'status': 'removed'})
            
            return JsonResponse({'status': 'added'})
    
    return JsonResponse({'status': 'error'})

@login_required
def private_rooms(request):
    """Display private rooms the user has joined"""
    # Get rooms owned by the user
    owned_rooms = ChatRoom.objects.filter(owner=request.user, room_type='private').order_by('-created_at')
    
    # Get rooms the user has joined
    joined_memberships = PrivateRoomMembership.objects.filter(user=request.user).select_related('room')
    joined_rooms = [membership.room for membership in joined_memberships if membership.room.owner != request.user]
    
    return render(request, 'chatapp/private_rooms.html', {
        'owned_rooms': owned_rooms,
        'joined_rooms': joined_rooms
    })

@login_required
def join_private_room(request):
    """Join a private room using access code"""
    if request.method == 'POST':
        access_code = request.POST.get('access_code', '').strip().upper()
        
        if not access_code:
            messages.error(request, 'Please enter an access code')
            return render(request, 'chatapp/join_private_room.html')
        
        try:
            room = ChatRoom.objects.get(access_code=access_code, room_type='private')
            
            # Check if user is already a member
            if PrivateRoomMembership.objects.filter(user=request.user, room=room).exists():
                messages.info(request, 'You are already a member of this room')
                return redirect('chatroom', slug=room.slug)
            
            # Add user to the room
            PrivateRoomMembership.objects.create(user=request.user, room=room)
            messages.success(request, f'Successfully joined "{room.name}"!')
            return redirect('chatroom', slug=room.slug)
            
        except ChatRoom.DoesNotExist:
            messages.error(request, 'Invalid access code. Please check and try again.')
    
    return render(request, 'chatapp/join_private_room.html')

@login_required
def leave_private_room(request, slug):
    """Leave a private room"""
    room = get_object_or_404(ChatRoom, slug=slug, room_type='private')
    
    # Room owner cannot leave their own room
    if room.owner == request.user:
        messages.error(request, 'You cannot leave a room you own. You can delete it instead.')
        return redirect('private_rooms')
    
    # Remove membership
    membership = PrivateRoomMembership.objects.filter(user=request.user, room=room).first()
    if membership:
        membership.delete()
        messages.success(request, f'You have left "{room.name}"')
    
    return redirect('private_rooms')

@login_required
def delete_private_room(request, slug):
    """Delete a private room (only owner can delete)"""
    room = get_object_or_404(ChatRoom, slug=slug, room_type='private', owner=request.user)
    
    if request.method == 'POST':
        room_name = room.name
        room.delete()
        messages.success(request, f'Room "{room_name}" has been deleted successfully.')
        return redirect('private_rooms')
    
    return render(request, 'chatapp/confirm_delete_room.html', {'room': room})

@login_required
def setup_google_oauth(request):
    """Setup Google OAuth configuration guide"""
    return render(request, 'chatapp/setup_google_oauth.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create the user using the form's save method
                user = form.save()
                
                # Log the user in automatically after successful registration
                login(request, user)
                
                messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
                return redirect('index')
                
            except Exception as e:
                messages.error(request, f'An error occurred while creating your account: {str(e)}')
                return render(request, 'chatapp/register.html', {'form': form})
        else:
            # Form has validation errors
            return render(request, 'chatapp/register.html', {'form': form})
    else:
        form = CustomRegistrationForm()
    
    return render(request, 'chatapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'chatapp/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

@login_required
def create_room(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        room_type = request.POST.get('room_type', 'public')
        room_slug = slugify(room_name)
        
        if ChatRoom.objects.filter(slug=room_slug).exists():
            messages.error(request, 'Room with this name already exists')
            return render(request, 'chatapp/create_room.html')
        
        room = ChatRoom.objects.create(
            name=room_name,
            slug=room_slug,
            room_type=room_type,
            owner=request.user
        )
        
        messages.success(request, f'Room "{room_name}" created successfully!')
        return redirect('chatroom', slug=room_slug)
    
    return render(request, 'chatapp/create_room.html')
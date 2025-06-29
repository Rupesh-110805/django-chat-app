from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import models
from .models import UserBlock
import json


@staff_member_required
def block_user_form(request, user_id):
    """Custom form for blocking a user with predefined reasons"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        block_type = request.POST.get('block_type')
        custom_reason = request.POST.get('custom_reason', '').strip()
        
        # Use custom reason if provided, otherwise use predefined reason
        final_reason = custom_reason if custom_reason else reason
        
        if not final_reason:
            messages.error(request, 'Please provide a reason for blocking the user.')
            return render(request, 'admin/chatapp/block_user_form.html', {'user': user})
        
        # Remove existing blocks for this user
        UserBlock.objects.filter(user=user, is_active=True).update(is_active=False)
        
        # Create new block based on type
        if block_type == 'permanent':
            UserBlock.objects.create(
                user=user,
                blocked_by=request.user,
                reason=final_reason,
                block_type='permanent'
            )
            messages.success(request, f'User {user.username} has been permanently blocked.')
        else:
            # Temporary block
            duration_days = int(block_type)
            blocked_until = timezone.now() + timezone.timedelta(days=duration_days)
            UserBlock.objects.create(
                user=user,
                blocked_by=request.user,
                reason=final_reason,
                block_type='temporary',
                blocked_until=blocked_until
            )
            messages.success(request, f'User {user.username} has been blocked for {duration_days} day(s).')
        
        return redirect('admin:auth_user_changelist')
    
    # Predefined reasons
    predefined_reasons = [
        'Inappropriate behavior in chat',
        'Spam or excessive messaging',
        'Harassment of other users',
        'Violation of community guidelines',
        'Sharing inappropriate content',
        'Multiple warnings ignored',
        'Suspected bot or fake account',
        'Administrative discretion'
    ]
    
    # Check if user is already blocked
    current_block = UserBlock.objects.filter(user=user, is_active=True).first()
    
    context = {
        'user': user,
        'predefined_reasons': predefined_reasons,
        'current_block': current_block,
        'is_currently_blocked': current_block and current_block.is_currently_blocked if current_block else False
    }
    
    return render(request, 'admin/chatapp/block_user_form.html', context)


@staff_member_required
@require_POST
def quick_unblock_user(request, user_id):
    """Quick unblock user via AJAX"""
    user = get_object_or_404(User, id=user_id)
    
    updated_count = UserBlock.objects.filter(user=user, is_active=True).update(is_active=False)
    
    if updated_count > 0:
        messages.success(request, f'User {user.username} has been unblocked.')
        return JsonResponse({'success': True, 'message': f'User {user.username} unblocked successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'User was not blocked.'})


@staff_member_required
def blocked_users_dashboard(request):
    """Dashboard showing all blocked users"""
    active_blocks = UserBlock.objects.select_related('user', 'blocked_by').filter(
        is_active=True
    ).filter(
        models.Q(block_type='permanent') | models.Q(blocked_until__gt=timezone.now())
    ).order_by('-blocked_at')
    
    expired_blocks = UserBlock.objects.select_related('user', 'blocked_by').filter(
        block_type='temporary',
        is_active=False,
        blocked_until__lte=timezone.now()
    ).order_by('-blocked_until')[:20]  # Last 20 expired blocks
    
    context = {
        'active_blocks': active_blocks,
        'expired_blocks': expired_blocks,
        'total_active_blocks': active_blocks.count(),
    }
    
    return render(request, 'admin/chatapp/blocked_users_dashboard.html', context)

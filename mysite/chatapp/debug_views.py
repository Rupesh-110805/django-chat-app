from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def debug_auth_status(request):
    """Debug view to check authentication status"""
    return JsonResponse({
        'is_authenticated': request.user.is_authenticated,
        'user_id': request.user.id if request.user.is_authenticated else None,
        'username': request.user.username if request.user.is_authenticated else None,
        'email': request.user.email if request.user.is_authenticated else None,
        'session_key': request.session.session_key,
        'session_data': dict(request.session) if hasattr(request.session, '__iter__') else {}
    })

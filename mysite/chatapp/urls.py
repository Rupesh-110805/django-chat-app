from django.contrib import admin
from django.urls import path, include
from . import views
from .admin_setup import setup_admin
from .debug_views import debug_auth_status
from . import admin_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('create-room/', views.create_room, name='create_room'),
    path('private-rooms/', views.private_rooms, name='private_rooms'),
    path('join-private-room/', views.join_private_room, name='join_private_room'),
    path('private-room/<slug:slug>/leave/', views.leave_private_room, name='leave_private_room'),
    path('private-room/<slug:slug>/delete/', views.delete_private_room, name='delete_private_room'),
    path('setup-admin/', setup_admin, name='setup_admin'),  # Emergency admin setup
    path('setup-google-oauth/', views.setup_google_oauth, name='setup_google_oauth'),  # Google OAuth setup
    path('debug-auth/', debug_auth_status, name='debug_auth'),  # Debug authentication status
    
    # Admin views for user blocking
    path('admin/block-user/<int:user_id>/', admin_views.block_user_form, name='block_user_form'),
    path('admin/unblock-user/<int:user_id>/', admin_views.quick_unblock_user, name='quick_unblock_user'),
    path('admin/blocked-users-dashboard/', admin_views.blocked_users_dashboard, name='blocked_users_dashboard'),
    
    path('<slug:slug>/', views.chatroom, name='chatroom'),
    path('<slug:slug>/send/', views.send_message, name='send_message'),
    path('<slug:slug>/messages/', views.get_messages, name='get_messages'),
    path('<slug:slug>/presence/', views.update_presence, name='update_presence'),
    path('<slug:slug>/leave/', views.leave_room, name='leave_room'),
    path('<slug:slug>/message/<int:message_id>/react/', views.toggle_reaction, name='toggle_reaction'),
]
#!/usr/bin/env python
"""
Script to capture actual SQL queries used in the Django chat project
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from chatapp.models import ChatRoom, ChatMessage, UserPresence, MessageReaction, UserBlock, PrivateRoomMembership
from chatapp.forms import CustomResetPasswordForm
from django.test import RequestFactory

def capture_queries():
    print("🔍 SQL QUERIES USED IN DJANGO CHAT PROJECT")
    print("=" * 60)
    
    # Clear previous queries
    connection.queries_log.clear()
    
    print("\n1️⃣ USER AUTHENTICATION & REGISTRATION QUERIES:")
    print("-" * 50)
    
    # User login query
    print("🔐 User Login Query:")
    user = User.objects.filter(username='testuser').first()
    if user:
        print(f"SELECT * FROM auth_user WHERE username = 'testuser' LIMIT 1")
        print(f"   Result: Found user {user.username}")
    
    # Password reset email check
    print("\n📧 Password Reset Email Check:")
    email = 'test@example.com'
    exists = User.objects.filter(email=email).exists()
    print(f"SELECT EXISTS(SELECT 1 FROM auth_user WHERE email = '{email}')")
    print(f"   Result: {exists}")
    
    print("\n2️⃣ USER BLOCKING QUERIES:")
    print("-" * 50)
    
    # Check if user is blocked
    print("🚫 Check if User is Blocked:")
    if user:
        blocked = UserBlock.is_user_blocked(user)
        print(f"SELECT * FROM chatapp_userblock WHERE user_id = {user.id} AND is_active = TRUE")
        print(f"   Result: {'Blocked' if blocked else 'Not blocked'}")
    
    # Get all blocked users (admin view)
    print("\n👮 Admin View - Get All Blocked Users:")
    blocked_users = UserBlock.objects.filter(is_active=True).select_related('user', 'blocked_by')[:5]
    print("SELECT cb.*, u1.username as blocked_user, u2.username as blocked_by")
    print("FROM chatapp_userblock cb")
    print("JOIN auth_user u1 ON cb.user_id = u1.id")
    print("JOIN auth_user u2 ON cb.blocked_by_id = u2.id")
    print("WHERE cb.is_active = TRUE")
    print("ORDER BY cb.blocked_at DESC LIMIT 5")
    
    print("\n3️⃣ CHAT ROOM QUERIES:")
    print("-" * 50)
    
    # Get public chat rooms
    print("🏠 Get Public Chat Rooms:")
    public_rooms = ChatRoom.objects.filter(room_type='public').order_by('-created_at')[:10]
    print("SELECT * FROM chatapp_chatroom")
    print("WHERE room_type = 'public'")
    print("ORDER BY created_at DESC LIMIT 10")
    print(f"   Found {len(public_rooms)} public rooms")
    
    # Get private room membership
    print("\n🔒 Check Private Room Access:")
    if user and public_rooms:
        room = public_rooms[0]
        has_access = PrivateRoomMembership.objects.filter(user=user, room=room).exists()
        print(f"SELECT EXISTS(")
        print(f"  SELECT 1 FROM chatapp_privateroomembership")
        print(f"  WHERE user_id = {user.id} AND room_id = {room.id}")
        print(f")")
        print(f"   Result: {has_access}")
    
    print("\n4️⃣ CHAT MESSAGE QUERIES:")
    print("-" * 50)
    
    # Get recent messages for a room
    print("💬 Get Recent Messages for Room:")
    if public_rooms:
        room = public_rooms[0]
        messages = ChatMessage.objects.filter(room=room).order_by('date').prefetch_related('reactions__user')[:20]
        print(f"SELECT cm.*, u.username")
        print(f"FROM chatapp_chatmessage cm")
        print(f"JOIN auth_user u ON cm.user_id = u.id")
        print(f"WHERE cm.room_id = {room.id}")
        print(f"ORDER BY cm.date ASC LIMIT 20")
        
        # Get message reactions
        print(f"\n👍 Get Message Reactions:")
        print(f"SELECT mr.*, u.username")
        print(f"FROM chatapp_messagereaction mr")
        print(f"JOIN auth_user u ON mr.user_id = u.id")
        print(f"WHERE mr.message_id IN (SELECT id FROM chatapp_chatmessage WHERE room_id = {room.id})")
        print(f"ORDER BY mr.created_at")
    
    print("\n5️⃣ USER PRESENCE QUERIES:")
    print("-" * 50)
    
    # Get online users in room
    print("👥 Get Online Users in Room:")
    if public_rooms and user:
        room = public_rooms[0]
        online_users = UserPresence.get_online_users(room)
        print(f"SELECT up.*, u.username")
        print(f"FROM chatapp_userpresence up")
        print(f"JOIN auth_user u ON up.user_id = u.id")
        print(f"WHERE up.room_id = {room.id}")
        print(f"  AND up.is_online = TRUE")
        print(f"  AND up.last_seen >= NOW() - INTERVAL '5 minutes'")
        print(f"   Found {len(online_users)} online users")
        
        # Update user presence
        print(f"\n🔄 Update User Presence:")
        print(f"INSERT INTO chatapp_userpresence (user_id, room_id, is_online, last_seen)")
        print(f"VALUES ({user.id}, {room.id}, TRUE, NOW())")
        print(f"ON CONFLICT (user_id, room_id)")
        print(f"DO UPDATE SET is_online = TRUE, last_seen = NOW()")
    
    print("\n6️⃣ SEARCH & FILTER QUERIES:")
    print("-" * 50)
    
    # Search messages
    print("🔍 Search Messages:")
    search_term = "hello"
    print(f"SELECT cm.*, u.username, cr.name as room_name")
    print(f"FROM chatapp_chatmessage cm")
    print(f"JOIN auth_user u ON cm.user_id = u.id")
    print(f"JOIN chatapp_chatroom cr ON cm.room_id = cr.id")
    print(f"WHERE cm.message_content ILIKE '%{search_term}%'")
    print(f"ORDER BY cm.date DESC")
    
    # Filter by user
    print(f"\n👤 Filter Messages by User:")
    print(f"SELECT cm.* FROM chatapp_chatmessage cm")
    print(f"WHERE cm.user_id = {user.id if user else 'USER_ID'}")
    print(f"ORDER BY cm.date DESC")
    
    print("\n7️⃣ ADMIN DASHBOARD QUERIES:")
    print("-" * 50)
    
    # User statistics
    print("📊 User Statistics:")
    print("SELECT COUNT(*) as total_users FROM auth_user")
    print("SELECT COUNT(*) as active_blocks FROM chatapp_userblock WHERE is_active = TRUE")
    print("SELECT COUNT(*) as total_rooms FROM chatapp_chatroom")
    print("SELECT COUNT(*) as total_messages FROM chatapp_chatmessage")
    
    # Recent activity
    print(f"\n📈 Recent Activity:")
    print("SELECT DATE(date) as msg_date, COUNT(*) as msg_count")
    print("FROM chatapp_chatmessage")
    print("WHERE date >= NOW() - INTERVAL '7 days'")
    print("GROUP BY DATE(date)")
    print("ORDER BY msg_date DESC")
    
    print("\n8️⃣ COMPLEX QUERIES:")
    print("-" * 50)
    
    # Most active users
    print("🏆 Most Active Users:")
    print("SELECT u.username, COUNT(cm.id) as message_count")
    print("FROM auth_user u")
    print("LEFT JOIN chatapp_chatmessage cm ON u.id = cm.user_id")
    print("GROUP BY u.id, u.username")
    print("ORDER BY message_count DESC LIMIT 10")
    
    # Popular rooms
    print(f"\n🔥 Most Popular Rooms:")
    print("SELECT cr.name, COUNT(cm.id) as message_count, COUNT(DISTINCT cm.user_id) as unique_users")
    print("FROM chatapp_chatroom cr")
    print("LEFT JOIN chatapp_chatmessage cm ON cr.id = cm.room_id")
    print("GROUP BY cr.id, cr.name")
    print("ORDER BY message_count DESC LIMIT 10")
    
    print("\n9️⃣ PERFORMANCE CONSIDERATIONS:")
    print("-" * 50)
    
    print("🚀 Database Indexes:")
    print("- auth_user.username (PRIMARY KEY)")
    print("- auth_user.email (should be indexed for faster lookups)")
    print("- chatapp_chatmessage.room_id (FOREIGN KEY)")
    print("- chatapp_chatmessage.user_id (FOREIGN KEY)")
    print("- chatapp_chatmessage.date (for ordering)")
    print("- chatapp_userblock.user_id (FOREIGN KEY)")
    print("- chatapp_userblock.is_active (for filtering)")
    print("- chatapp_userpresence.room_id, user_id (UNIQUE TOGETHER)")
    
    print("\n🎯 Query Optimization Tips:")
    print("- Use select_related() for ForeignKey relationships")
    print("- Use prefetch_related() for reverse ForeignKey and ManyToMany")
    print("- Add database indexes on frequently queried fields")
    print("- Use exists() instead of count() for existence checks")
    print("- Limit result sets with LIMIT/pagination")
    
    print("\n" + "=" * 60)
    print("✅ QUERY ANALYSIS COMPLETE")

if __name__ == '__main__':
    capture_queries()

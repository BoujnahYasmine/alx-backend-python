from django.urls import path
from .views import delete_user
from .views import conversation_thread, unread_messages_view

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
    path('thread/<int:message_id>/', conversation_thread, name='conversation_thread'),
    path('unread-messages/', unread_messages_view, name='unread_messages'),
    
]
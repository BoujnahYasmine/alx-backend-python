from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Message


@login_required
def unread_messages_view(request):
    """View to fetch all unread messages for a user."""
    unread_messages = Message.unread.unread_for_user(request.user).only('sender', 'content', 'timestamp')
    return render(request, 'chat/unread_messages.html', {'unread_messages': unread_messages})

@login_required
@cache_page(60)
def conversation_thread(request, message_id):
    """View to fetch a message and its replies using prefetch_related."""
    message = get_object_or_404(
        Message.objects.prefetch_related('replies').select_related('sender', 'receiver')
        .filter(sender=request.user) | Message.objects.filter(receiver=request.user), 
        id=message_id
    )
    context = {'message': message, 'replies': message.get_all_replies()}
    return render(request, 'chat/conversation_thread.html', context)

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return JsonResponse({"message": "Your account has been deleted successfully."})

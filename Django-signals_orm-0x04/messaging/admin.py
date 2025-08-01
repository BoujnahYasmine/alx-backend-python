from django.contrib import admin
from .models import Message, Notification, MessageHistory

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content', 'receiver', 'edited', 'timestamp', 'read', 'id')
    search_fields = ('sender__username', 'receiver__username')
    def get_queryset(self, request):
        """
        Restrict each admin and user to see only their own Sent messages,
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(sender=request.user)
        return qs.filter(sender=request.user)


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'old_content', 'edited_at', 'edited_by')
   

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'is_read', 'created_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        """
        Restrict each admin and user to see only their own notifications.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs.filter(user=request.user)
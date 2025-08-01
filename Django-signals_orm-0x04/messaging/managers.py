from django.db import models

class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        """Retrieve only unread messages."""
        return super().get_queryset().filter(read=False)

    def unread_for_user(self, user):
        """Filter unread messages for a specific user with only necessary fields."""
        return self.get_queryset().filter(receiver=user).only('sender', 'content', 'timestamp')
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from .models import Question
from notifications.models import Notification


@receiver(post_save, sender=Question)
def create_notification_on_approval(sender, instance, created, **kwargs):
    """
    Create a notification when a question is approved.
    """
    if created:
        return

    if instance.status == 'APPROVED':
        # Prevent duplicate notifications
        already_notified = Notification.objects.filter(
            user=instance.author,
            message__icontains=instance.title
        ).exists()

        if not already_notified:
            Notification.objects.create(
                user=instance.author,
                message=f'Your question "{instance.title}" has been approved.',
                link=reverse('questions:detail', kwargs={'pk': instance.pk})
            )

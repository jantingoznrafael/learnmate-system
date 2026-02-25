from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.urls import reverse
from questions.models import Question
from .models import Notification

User = get_user_model()


@receiver(pre_save, sender=Question)
def track_previous_status(sender, instance, **kwargs):
    if instance.pk:
        previous = Question.objects.get(pk=instance.pk)
        instance._previous_status = previous.status
    else:
        instance._previous_status = None


@receiver(post_save, sender=Question)
def notify_question_approved(sender, instance, created, **kwargs):
    if (
        instance.status == 'APPROVED'
        and instance._previous_status != 'APPROVED'
    ):
        question_url = reverse('questions:detail', kwargs={'pk': instance.pk})

        Notification.objects.get_or_create(
            user=instance.author,
            message=f'Your question "{instance.title}" has been approved!',
            link=question_url
        )

        if instance.strand != 'ALL':
            users_in_strand = User.objects.filter(
                strand=instance.strand
            ).exclude(pk=instance.author.pk)

            for user in users_in_strand:
                Notification.objects.get_or_create(
                    user=user,
                    message=f'A new {instance.strand} question: "{instance.title}"',
                    link=question_url
                )


@receiver(pre_save, sender=User)
def notify_profile_updated(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return

    if (
        old_instance.strand != instance.strand
        or old_instance.bio != instance.bio
        or old_instance.first_name != instance.first_name
        or old_instance.last_name != instance.last_name
    ):
        Notification.objects.get_or_create(
            user=instance,
            message='Your profile has been updated successfully.',
            link='/accounts/profile/'
        )

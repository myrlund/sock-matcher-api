from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SockMatch, SockPreference


@receiver(post_save, sender=SockPreference)
def maybe_create_match_object(sender, instance, created, **kwargs):

    if not instance.is_match:
        return

    if instance.source_sock.has_match:
        return

    SockMatch.objects.get_or_create(
        sock1=instance.source_sock,
        sock2=instance.target_sock,
    )

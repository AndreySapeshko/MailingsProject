from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.cache_utils import clear_cache
from mailings.models import Mailing, Message, Recipient

MODEL_CACHE_MAP = {
    Mailing: ["mailings", "api/mailings"],
    Message: ["messages", "api/messages"],
    Recipient: ["recipients", "api/recipients"],
}

@receiver([post_save, post_delete])
def clear_related_cache(sender, **kwargs):
    prefixes = MODEL_CACHE_MAP.get(sender)
    if prefixes:
        for prefix in prefixes:
            clear_cache(pattern=f"{prefix}*")

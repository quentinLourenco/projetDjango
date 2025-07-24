# boutique/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Commande

@receiver(post_save, sender=Commande)
def notifier_validation_commande(sender, instance, created, **kwargs):
    if instance.validee:
        print(f"📢 Notification : commande #{instance.id} validée pour {instance.client.username}")
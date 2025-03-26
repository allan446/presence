from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Permission

@receiver(post_save, sender=Permission)
def update_permission_status(sender, instance, **kwargs):
    # Vérifier si la date de fin est passée
    if instance.end_date < timezone.now().date():
        # Mettre à jour l'état de la permission
        instance.etat = 'terminer'
        instance.save()

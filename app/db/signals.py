from django.db.models.signals import post_delete
from django.dispatch import receiver

from db.models import ProductCode


@receiver(post_delete, sender=ProductCode)
def delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)
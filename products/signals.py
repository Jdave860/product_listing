# products/signals.py
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == 'products':  # Ensure this only runs for the products app
        Group.objects.get_or_create(name='Buyer')
        Group.objects.get_or_create(name='Supplier')
        Group.objects.get_or_create(name='Administrator')

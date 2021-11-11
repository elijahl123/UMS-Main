import stripe
from django.db import models
from django.dispatch import receiver

from UMSMain import settings
from users.models import Account

stripe.api_key = settings.STRIPE_API_KEY
from django.db.models.signals import post_save


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    stripe_customer_id = models.CharField(max_length=120)
    subscription_id = models.CharField(max_length=120, null=True)


@receiver(post_save, sender=Account)
def _on_update_user(sender, instance, created, **kwargs):
    if created or not CustomerProfile.objects.filter(user=instance).exists():  # If a new user is created

        # Create Stripe user
        customer = stripe.Customer.create(
            email=instance.email,
            name=instance,
            metadata={
                'user_id': instance.pk,
                'username': instance.username
            },
            description='Created from Django',
        )

        # Create profile
        profile = CustomerProfile.objects.create(user=instance, stripe_customer_id=customer.id)
        profile.save()

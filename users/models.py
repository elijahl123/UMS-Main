from typing import Union

import pytz
import stripe
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
from UMSMain.get_settings import settings

stripe.api_key = settings.STRIPE_API_KEY

color_choices = [
    ('primary', 'Blue'),
    ('secondary', 'Gray'),
    ('success', 'Green'),
    ('danger', 'Red'),
    ('warning', 'Yellow'),
    ('info', 'Light Blue'),
]


def upload_profile_picture(instance, filename):
    file_path = 'profilePictures/{username}/{filename}'.format(
        username=str(instance.username), filename=filename
    )
    return file_path


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a First Name')
        if not last_name:
            raise ValueError('Users must have a Last Name')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    school = models.CharField(null=True, blank=False, max_length=200)
    timezone = models.CharField(null=True, choices=[(tz, tz.replace('_', ' ')) for tz in pytz.all_timezones],
                                max_length=120)
    exempt_from_payment = models.BooleanField(default=False)
    show_schedule_on_calendar = models.BooleanField(default=False, verbose_name='Show Schedule on Calendar')
    send_scheduled_emails = models.BooleanField(default=False, verbose_name='Send Daily Summaries')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    class Meta:
        ordering = ['email']
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.email if not self.first_name and not self.last_name else f'{self.first_name} {self.last_name}'

        # For checking permissions. to keep it simple all admin have ALL permissions

    def subscription(self, expand: list = None) -> stripe.Subscription:
        from payments.models import CustomerProfile
        if CustomerProfile.objects.filter(user=self, subscription_id__isnull=False).exists():
            customer = CustomerProfile.objects.get(user=self)
            if expand:
                subscription = stripe.Subscription.retrieve(customer.subscription_id, expand=expand)
            else:
                subscription = stripe.Subscription.retrieve(customer.subscription_id)
            return subscription
        return None

    def customer_id(self) -> str:
        from payments.models import CustomerProfile
        if CustomerProfile.objects.filter(user=self, subscription_id__isnull=False).exists():
            customer = CustomerProfile.objects.get(user=self)
            return customer.stripe_customer_id
        return None

    def check_sub_status(self):
        if self.exempt_from_payment:
            return True
        if self.subscription():
            if self.subscription().status == 'active':
                return True
        return False

    def check_payment_status(self):
        if self.exempt_from_payment:
            return True
        if self.subscription():
            if self.subscription().default_payment_method:
                return True
        return False

    def has_perm(self, perm, obj=None):
        return self.is_admin

        # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)

    @staticmethod
    def has_module_perms(app_label):
        return True

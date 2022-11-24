import graphene
from graphene_django import DjangoObjectType

from users.models import Account


class AccountType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Account
        fields = (
            'uid',
            'first_name',
            'last_name',
            'username',
            'email',
            'date_joined',
            'last_login',
            'is_active',
            'is_admin',
            'is_staff',
            'is_superuser',
            'school',
            'timezone',
            'exempt_from_payment',
            'show_schedule_on_calendar',
            'send_scheduled_emails',
            'homework_notifications',
            'class_notifications',
        )
        filter_fields = [
            'uid',
            'first_name',
            'last_name',
            'username',
            'email',
            'date_joined',
            'last_login',
            'is_active',
            'is_admin',
            'is_staff',
            'is_superuser',
            'school',
            'timezone',
            'exempt_from_payment',
            'show_schedule_on_calendar',
            'send_scheduled_emails',
            'homework_notifications',
            'class_notifications',
        ]
        interfaces = (graphene.relay.Node,)

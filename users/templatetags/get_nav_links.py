import datetime

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from courses.models import CourseTime, Course
from notes.models import Note

register = template.Library()


@register.simple_tag(takes_context=True)
def get_nav_links(context, request):

    nav_links = [
        {
            "name": 'Account Info',
            "icon": "fas fa-user",
            "url": reverse('account'),
        },
        {
            "name": 'Account Settings',
            "icon": "fas fa-cog",
            "url": reverse('account_settings')
        },
        {
            "name": 'Change Email',
            "icon": "fas fa-envelope",
            "url": reverse('account_email')
        },
        {
            "name": 'Change Password',
            "icon": "fas fa-lock",
            "url": reverse('account_change_password')
        },
        {
            "name": 'Linked Accounts',
            "icon": "fas fa-link",
            "url": reverse('socialaccount_connections')
        },
    ]

    if not request.user.exempt_from_payment:
        nav_links[2] = {
            "name": 'Subscription',
            "icon": "fas fa-wallet",
            "url": reverse('account_subscription')
        }

    for link in nav_links:
        link['selected'] = True if request.path == link['url'] else False

    context['nav_links'] = nav_links

    return ''

from django.conf.urls import url
from django.urls import path

from payments.views import *

urlpatterns = [
    url(r'^create-subscription/(monthly|yearly)/', create_subscription, name='create_subscription'),
    url(r'^checkout/(monthly|yearly)/', checkout, name='payment_checkout'),
    path('status/', status, name='payment_status'),
    path('choose-plan/', choose_plan, name='choose_plan'),
    path('webhook/', stripe_webhooks, name='payment_webhook'),
]

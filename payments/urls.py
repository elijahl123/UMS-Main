from django.urls import path

from payments.views import *

urlpatterns = [
    path('create-subscription/', create_subscription, name='create_subscription'),
    path('checkout/', checkout, name='payment_checkout'),
    path('status/', status, name='payment_status'),
    path('webhook/', stripe_webhooks, name='payment_webhook'),
]

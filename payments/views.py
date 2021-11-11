# Create your views here.

import stripe
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from UMSMain import settings
from UMSMain.generic_class_views import school_required, timezone_required
from payments.models import CustomerProfile

context = {}

stripe.api_key = settings.STRIPE_API_KEY


@login_required
@require_http_methods(['POST'])
def create_subscription(request):
    # Create the subscription. Note we're expanding the Subscription's
    # latest invoice and that invoice's payment_intent
    # so we can pass it to the front end to confirm the payment
    customer = get_object_or_404(CustomerProfile, user=request.user)
    subscription = stripe.Subscription.create(
        customer=customer.stripe_customer_id,
        items=[{
            'price': settings.STRIPE_SUBSCRIPTION_PRICE_ID
        }],
        payment_behavior='default_incomplete',
        expand=['latest_invoice.payment_intent'],
    )
    customer.subscription_id = subscription.id
    customer.save()

    return JsonResponse({
        'subscriptionId': subscription.id,
        'clientSecret': subscription.latest_invoice.payment_intent.client_secret,
        'stripePublicKey': settings.STRIPE_PUBLIC_KEY
    })


@login_required
def checkout(request):
    context['account'] = request.user
    return render(request, 'payments/checkout.html', context)


@login_required
def status(request):
    context['account'] = request.user

    if request.POST:
        return JsonResponse({
            'stripePublicKey': settings.STRIPE_PUBLIC_KEY
        })

    return render(request, 'payments/status.html', context)


@csrf_exempt
def stripe_webhooks(request):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        try:
            signature = request.headers.get('Stripe-Signature')
            event = stripe.Webhook.construct_event(payload=request.body, sig_header=signature, secret=webhook_secret)
            data = event['data']
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event['type']
        except Exception as e:
            return JsonResponse({'error': e.user_message})
    else:
        data = None
        event_type = None

    data_object = data['object']

    if event_type == 'invoice.paid':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        print(data)

    if event_type == 'invoice.payment_failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        print(data)

    if event_type == 'customer.subscription.deleted':
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        print(data)

    if event_type == 'invoice.payment_succeeded':
        if data_object['billing_reason'] == 'subscription_create':
            subscription_id = data_object['subscription']
            payment_intent_id = data_object['payment_intent']

            # Retrieve the payment intent used to pay the subscription
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Set the default payment method
            stripe.Subscription.modify(
                subscription_id,
                default_payment_method=payment_intent.payment_method
            )

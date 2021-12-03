# Create your views here.

import stripe
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from UMSMain.generic_class_views import all_permissions_required
from UMSMain.get_settings import settings
from payments.models import CustomerProfile

context = {}

stripe.api_key = settings.STRIPE_API_KEY


@login_required
def choose_plan(request):
    context['account'] = request.user
    context['interval'] = None
    return render(request, 'payments/choose_plan.html', context)


@login_required
def checkout(request, payment_type: str):
    context['account'] = request.user
    context['type'] = payment_type

    if request.user.subscription():
        if request.user.subscription().status == 'active':
            return redirect('index')

    if request.POST:
        customer = get_object_or_404(CustomerProfile, user=request.user)
        subscription = stripe.Subscription.create(
            customer=customer.stripe_customer_id,
            items=[{
                'price': settings.STRIPE_SUBSCRIPTION_PRICE_ID_YEARLY if payment_type == 'yearly' else settings.STRIPE_SUBSCRIPTION_PRICE_ID_MONTHLY
            }],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent']
        )
        customer.subscription_id = subscription.id
        customer.save()
        return JsonResponse({
            'subscriptionId': subscription.id,
            'clientSecret': subscription.latest_invoice.payment_intent.client_secret,
            'stripePublicKey': settings.STRIPE_PUBLIC_KEY
        })

    return render(request, 'payments/checkout.html', context)


@login_required
def status(request):
    context['account'] = request.user

    if request.POST:
        return JsonResponse({
            'stripePublicKey': settings.STRIPE_PUBLIC_KEY
        })
    else:
        pm = stripe.PaymentIntent.retrieve(request.GET.get('payment_intent')).payment_method
        stripe.Subscription.modify(request.user.subscription().id, default_payment_method=pm)

    return render(request, 'payments/status.html', context)


@login_required
@all_permissions_required
def edit_plan(request):
    context['account'] = request.user

    subscription = request.user.subscription(['latest_invoice.payment_intent']).to_dict_recursive()

    context['interval'] = subscription['items']['data'][0]['plan']['interval']

    return render(request, 'payments/edit_subscription.html', context)


@login_required
@all_permissions_required
def change_plan_to(request, payment_type: str):
    context['account'] = request.user

    subscription = request.user.subscription(['latest_invoice.payment_intent'])

    payment_method_id = stripe.PaymentIntent.retrieve(
        request.user.subscription(['latest_invoice']).latest_invoice.payment_intent).payment_method

    stripe.Subscription.modify(
        subscription.id,
        items=[{
            'id': subscription['items']['data'][0].id,
            'price': settings.STRIPE_SUBSCRIPTION_PRICE_ID_YEARLY if payment_type == 'yearly' else settings.STRIPE_SUBSCRIPTION_PRICE_ID_MONTHLY
        }],
        cancel_at_period_end=False,
        proration_behavior='none',
        default_payment_method=payment_method_id,
        expand=['latest_invoice.payment_intent']
    )
    return redirect('account_subscription')


@login_required
@all_permissions_required
def cancel_subscription(request):
    context['account'] = request.user

    subscription = request.user.subscription()

    stripe.Subscription.modify(
        subscription.id,
        cancel_at_period_end=True
    )

    return redirect('account_subscription')


@login_required
@all_permissions_required
def resume_subscription(request):
    context['account'] = request.user

    subscription = request.user.subscription()

    stripe.Subscription.modify(
        subscription.id,
        cancel_at_period_end=False
    )

    return redirect('account_subscription')


@login_required
@all_permissions_required(exclude=['payment_method'])
def edit_payment_method(request):
    context['account'] = request.user

    if request.POST:
        customer = get_object_or_404(CustomerProfile, user=request.user)
        setup = stripe.SetupIntent.create(customer=customer.stripe_customer_id)
        return JsonResponse({
            'setupID': setup.id,
            'clientSecret': setup.client_secret,
            'stripePublicKey': settings.STRIPE_PUBLIC_KEY
        })

    if 'setup_intent' in request.GET and 'setup_intent_client_secret' in request.GET:
        setup = stripe.SetupIntent.retrieve(id=request.GET.get('setup_intent'))
        subscription = request.user.subscription()
        stripe.Subscription.modify(
            subscription.id,
            default_payment_method=setup.payment_method
        )
        if request.GET.get('next'):
            return HttpResponseRedirect(request.GET.get('next'))
        return redirect('account_subscription')

    return render(request, 'payments/edit_payment_method.html', context)


@login_required
@all_permissions_required
def delete_payment_method(request):
    context['account'] = request.user

    subscription = request.user.subscription()

    stripe.Subscription.modify(
        subscription.id,
        default_payment_method=''
    )

    return redirect('account_subscription')


@csrf_exempt
def stripe_webhooks(request):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    if webhook_secret:
        try:
            signature = request.headers.get('Stripe-Signature')
            event = stripe.Webhook.construct_event(payload=request.body, sig_header=signature, secret=webhook_secret)
            data = event['data']
            event_type = event['type']
        except Exception as e:
            return JsonResponse({'error': e.user_message})
    else:
        data = None
        event_type = None

    data_object = data['object']

    if event_type == 'payment_method.attached':
        customer = stripe.Customer.retrieve(data_object['customer'])
        if customer.email:
            email_context = {
                'current_site': get_current_site(request)
            }
            message = EmailMessage(
                subject='New Payment Method Attatched to Account',
                body=render_to_string('email/payment_method.attached.txt', context=email_context),
                from_email=settings.ADMIN_EMAIL,
                to=[customer.email]
            )
            message.send()

    if event_type == 'invoice.paid':
        if data_object['billing_reason'] == 'subscription_create':
            customer = stripe.Customer.retrieve(data_object['customer'])
            if customer.email:
                email_context = {
                    'current_site': get_current_site(request),
                    'amount': f"{int(data_object['lines']['data'][0]['amount']) / 100:.2f}"
                }
                message = EmailMessage(
                    subject='Successfully Subscribed to UMS',
                    body=render_to_string('email/invoice.paid.txt', context=email_context),
                    from_email=settings.ADMIN_EMAIL,
                    to=[customer.email]
                )
                message.send()

    if event_type == 'customer.subscription.updated':
        print(data_object)

    return JsonResponse({'status': 'succeeded'})

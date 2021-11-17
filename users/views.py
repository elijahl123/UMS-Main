import datetime

import pytz
import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from UMSMain import settings
from UMSMain.generic_class_views import all_permissions_required
from payments.models import CustomerProfile
from users.forms import AccountForm, AccountSettings
from users.models import Account

context = {}

stripe.api_key = settings.STRIPE_API_KEY


@login_required
@all_permissions_required
def account(request):
    context['account'] = request.user

    if request.POST:
        form = AccountForm(request.POST, request.FILES or None, instance=request.user)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, 'Account Changed Successfully')
            return redirect('account')
    else:
        form = AccountForm(instance=request.user)

    context['form'] = form

    return render(request, 'account.html', context)


@login_required
@all_permissions_required
def account_settings(request):
    context['account'] = request.user

    if request.POST:
        form = AccountSettings(request.POST, request.FILES or None, instance=request.user)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, 'Account Settings Changed Successfully')
            return redirect('account_settings')
    else:
        form = AccountSettings(instance=request.user)

    context['form'] = form

    return render(request, 'account_settings.html', context)


@login_required
@all_permissions_required
def change_account_calendar_view(request):
    if request.user.show_schedule_on_calendar:
        Account.objects.filter(id=request.user.id).update(show_schedule_on_calendar=False)
    else:
        Account.objects.filter(id=request.user.id).update(show_schedule_on_calendar=True)

    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect('index')


@login_required
def select_timezone(request):
    context['account'] = request.user
    today = datetime.datetime.today()

    def get_tz_str(tz):
        tz_obj = pytz.timezone(tz)
        obj = [*tz.replace('_', ' ').split('/')]
        obj[-1] = f'{tz_obj.localize(today).strftime("(UTC%z)")} {obj[-1]}'
        return obj

    timezones = [(tz, *get_tz_str(tz)) for tz in pytz.common_timezones]

    context['timezones'] = timezones

    if request.POST:
        user = get_object_or_404(Account, id=request.user.id)
        user.timezone = request.POST['timezone']
        user.save()
        messages.success(request, 'Timezone Selected Successfully')
        return redirect('index') if not request.GET.get('next') else HttpResponseRedirect(request.GET['next'])

    return render(request, 'set_up/add_timezone.html', context)


@login_required
@all_permissions_required
def account_subscription(request):
    context['account'] = request.user

    customer_info = CustomerProfile.objects.get(user=request.user)

    subscription = request.user.subscription_info(['latest_invoice.payment_intent']).to_dict_recursive()

    context['subscription'] = subscription

    amount = f"{subscription['items']['data'][0]['plan']['amount'] / 100:.2f}"

    current_period_end = datetime.datetime.fromtimestamp(subscription['current_period_end'])

    context['sub_info'] = {
        'amount': amount,
        'current_period_end': current_period_end
    }

    context['payment_intents'] = stripe.PaymentIntent.list(customer=customer_info.stripe_customer_id)

    print(context['payment_intents'])

    return render(request, 'account_subscription.html', context)

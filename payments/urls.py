from django.conf.urls import url
from django.urls import path

from payments.views import *

urlpatterns = [
    url(r'^checkout/(monthly|yearly)/', checkout, name='payment_checkout'),
    path('status/', status, name='payment_status'),
    path('choose-plan/', choose_plan, name='choose_plan'),
    path('edit-plan/', edit_plan, name='payment_edit_plan'),
    path('edit-payment-method/', edit_payment_method, name='payment_edit_payment_method'),
    path('delete-payment-method/', delete_payment_method, name='payment_delete_payment_method'),
    path('cancel-subscription/', cancel_subscription, name='payment_cancel_subscription'),
    path('resume-subscription/', resume_subscription, name='payment_resume_subscription'),
    url(r'^change-plan/to/(monthly|yearly)/', change_plan_to, name='payment_change_plan_to'),
    path('webhook/', stripe_webhooks, name='payment_webhook'),
]

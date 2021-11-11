from django.contrib import admin

# Register your models here.
from payments.models import CustomerProfile


@admin.register(CustomerProfile)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_customer_id',)
    list_filter = ('stripe_customer_id',)

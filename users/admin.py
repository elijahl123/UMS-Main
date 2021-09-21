from django.contrib import admin

# Register your models here.
from users.models import *

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'last_login', 'is_superuser')
    list_filter = ('last_name', )

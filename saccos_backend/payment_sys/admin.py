from django.contrib import admin
from payment_sys.models import Transaction, UserWallet, SaccosWallet

# Register your models here.
admin.site.register(Transaction)
admin.site.register(UserWallet)
admin.site.register(SaccosWallet)

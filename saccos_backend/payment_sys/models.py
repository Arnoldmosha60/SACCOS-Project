from django.db import models
from user_management.models import User
import uuid

# Create your models here.
class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet of {self.user.email}"

    class Meta:
        db_table = 'user_wallet'


class SaccosWallet(models.Model):
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return "Sacco's Wallet"

    class Meta:
        db_table = 'saccos_wallet'


class Transaction(models.Model):
    transaction_id = models.BigIntegerField(unique=True)
    created_at = models.DateTimeField()
    charge_response_code = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    charged_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    currency = models.CharField(max_length=20)
    tx_ref = models.CharField(max_length=100, unique=True)
    flw_ref = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment {self.transaction_id} => {self.customer.id}"

    class Meta:
        db_table = 'transaction'
        ordering = ['-created_at']


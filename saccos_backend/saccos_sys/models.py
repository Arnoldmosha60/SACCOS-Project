import uuid
from django.db import models
from user_management.models import User
from payment_sys.models import Transaction

# Create your models here.
class Share(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number_of_shares = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        db_table = 'share'


class Saving(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        db_table = 'saving'


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_date = models.DateTimeField()
    next_event_date = models.DateTimeField(null=True, blank=True)
    post_created_on = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    venue = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'events'


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    share = models.ForeignKey(Share, on_delete=models.CASCADE)
    # loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    generated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'report'



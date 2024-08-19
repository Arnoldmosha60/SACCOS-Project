from django.db import models
import uuid
from user_management.models import User

# Create your models here.
class Loan(models.Model):

    LOANSTATUS =(
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loanType = models.CharField(max_length=50)
    loanRequestAmount = models.DecimalField(max_digits=10, decimal_places=2) # kiasi cha mkopo kinachoombwa
    loanRequestDate = models.DateTimeField(auto_now_add=True) # tarehe ya maombi ya mkopo
    loanDescription = models.CharField(max_length=200)
    loanRepayDuration = models.CharField(max_length=30) # mkopo utalipwa ndani ya muda gani (miezi)
    loanRepayPerMonth = models.DecimalField(max_digits=10, decimal_places=2) # kiasi cha mkopo cha kulipa kila mwezi
    loanPaymentDeadline = models.DateTimeField(null=True, blank=True) # tarehe ya mwisho ya malipo ya mkopo(baada ya kuidhinishwa)
    loanStatus = models.CharField(choices=LOANSTATUS, default='PENDING')
    referee = models.CharField(max_length=50)
    loanRepaymentPlan = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_already_paid = models.DecimalField(max_digits=10, default=0.00, decimal_places=2, null=True, blank=True)
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        db_table = 'loan'


class LoanVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    verification_reason = models.CharField(max_length=200)
    verified_by = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_date = models.DateTimeField(auto_now_add=True)
    loan_verified_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Verification for {self.loan.id}"
    
    class Meta:
        db_table = "loan_verification"
    

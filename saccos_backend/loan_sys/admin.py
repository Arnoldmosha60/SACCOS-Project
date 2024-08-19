from django.contrib import admin
from .models import Loan, LoanVerification

# Register your models here.
admin.site.register(Loan)
admin.site.register(LoanVerification)

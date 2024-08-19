from django.urls import path
from .views import *

app_name = 'loan_sys'

urlpatterns = [
    path('loan-eligibility/', CheckLoanApplicationEligibilityView.as_view(), name="checking_loan_eligibility"),
    path('loan-application/', LoanApplicationView.as_view(), name="loan_application"),
    path('user-pending-loans/', UserPendingLoanList.as_view(), name="user_pending_loans"),
    path('all-pending-loans/', AllPendingLoansView.as_view(), name="all_pending_loans"),
    path('verify-loan/<uuid:loan_id>/', LoanVerificationView.as_view(), name='verify_loan'),
    path('approve-loan/<uuid:loan_id>/', ApproveLoanView.as_view(), name='approve_loan'),
    path('user-approved-loans/', UserApprovedLoanList.as_view(), name='user_approved_loans'),
    path('loan-history-data/', GetLoanHistoryData.as_view(), name="get_loan_history_data"),
    path('institute-loans/', InstitutionLoansAPIView.as_view(), name='get_loans_related_to_institution'),
]
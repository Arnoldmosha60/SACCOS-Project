from django.urls import path
from .views import *

app_name = 'payment_sys'

urlpatterns = [
    path('transactions/', TransactionView.as_view(), name="transactions"),
    path('get-user-kiingilio-transaction/<uuid:user_id>/', GetUserKiingilioTransactionView.as_view(), name="get_user_kiingilio_transaction"),
    path('transaction-history/', TransactionHistoryView.as_view(), name="transaction_history"),
    path('user-financial-data/<uuid:user_id>/', UserFinancialData.as_view(), name='user_financial_data'),
]
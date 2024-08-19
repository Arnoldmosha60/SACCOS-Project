from django.urls import path
from .views import *

app_name = 'saccos_sys'

urlpatterns = [
    path('get-mikoa-data/', GetMikoaData.as_view(), name="get_mikoa_data"),
    path('share-payment/', SharePaymentView.as_view(), name='share_payment'),
    path('all-shares/', AllShares.as_view(), name='all_shares'),
    path('saving-payment/', SavingPaymentView.as_view(), name='saving_payment'),
    path('all-savings/', AllSavings.as_view(), name='all_savings'),

    path('events', EventListCreateRetrieveUpdateDeleteView.as_view(), name='event-list-create'),
    path('events/<uuid:event_id>/', EventListCreateRetrieveUpdateDeleteView.as_view(), name='event-detail'),
    path('generate-report/<uuid:user_id>/', GenerateReportAPIView.as_view(), name='generate_report'),
]
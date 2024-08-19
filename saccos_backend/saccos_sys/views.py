import datetime
from decimal import Decimal
import json
import uuid
import requests
import logging
from django.shortcuts import get_object_or_404, render
from mtaa import tanzania
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from saccos_sys.models import Saving, Share, Event
from user_management.models import User
from rest_framework import status
from payment_sys.models import SaccosWallet, Transaction, UserWallet
from .serializers import SavingPaymentSerializer, SharePaymentSerializer, EventSerializer
from requests.auth import HTTPBasicAuth
from payment_sys.serializers import TransactionSerializer
from django.db import models
from rest_framework.authentication import TokenAuthentication
from django.db.models import Sum
from django.db import transaction as db_transaction
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from loan_sys.models import Loan

logger = logging.getLogger(__name__)

def send_sms(phone_number, membership_number, description, amount):
    phone_number = phone_number

    # Prepare SMS data
    if phone_number.startswith('0'):
        phone_number = '255' + phone_number[1:]
    
    data = {
        "source_addr": "INFO",
        "schedule_time": "",
        "encoding": 0,
        "message": f"Ndugu mwanachama mwenye namba {membership_number}, Malipo yako ya {description} kiasi cha shillingi {amount} yamekamilika.",
        "recipients": [
            {
                "recipient_id": 1,
                "dest_addr": phone_number
            }
        ]
    }

    # Send SMS
    try:
        username = "59e77c6f92ef3836"  
        password = "MmNkMmE0YjI4NjFiZDgwNjZkZDNmZWY0ZTU4YzA5ZThkZDFlODMwZGRmMmM4ZDYwMDg1YjVjNDUxYWM3ZmQyZQ=="  # Replace with actual password
        response = requests.post("https://apisms.beem.africa/v1/send", json=data, auth=HTTPBasicAuth(username, password))

        if response.status_code == 200:
            print("SMS sent successfully!")
            return Response({'message': 'SMS sent successfully'}, status=status.HTTP_200_OK)
        else:
            print(f"SMS sending failed. Status code: {response.status_code}, Response: {response.text}")
            return Response({'message': 'failed to send SMS'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")

# Create your views here.
class GetMikoaData(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        mikoa = list(tanzania)  # Get all regions
        wilaya = {region: list(tanzania.get(region).districts) for region in mikoa}
        kata = {region: {district: list(tanzania.get(region).districts.get(district).wards) for district in wilaya[region]} for region in mikoa}

        response = {
            'mikoa': mikoa,
            'wilaya': wilaya,
            'kata': kata,
        }
        return Response(response)


class SharePaymentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            print("User is authenticated:", user)
        else:
            print("User is not authenticated.")

        shares = Share.objects.filter(user=user).order_by('-date')
        total_amount = shares.aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
        serializer = SharePaymentSerializer(shares, many=True)
        response_data = {
            'success': True,
            "shares": serializer.data,
            "total_amount": total_amount
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data

            user_id = data.get('user', {}).get('id')
            if not user_id:
                return Response({'success': False, 'error': 'User data missing or invalid'}, status=400)
            
            user = get_object_or_404(User, id=user_id)

            transaction_data = data.get('successPaymentData', {})
                
            transaction = Transaction.objects.create(
                transaction_id=transaction_data.get('transaction_id'),
                created_at=transaction_data.get('created_at'),
                charge_response_code=transaction_data.get('charge_response_code'),
                amount=transaction_data.get('amount'),
                charged_amount=transaction_data.get('charged_amount'),
                description=transaction_data.get('description'),
                currency=transaction_data.get('currency'),
                tx_ref=transaction_data.get('tx_ref'),
                flw_ref=transaction_data.get('flw_ref'),
                status=transaction_data.get('status'),
                customer=user,
            )

            share_amount = data.get('requestObj', {}).get('amount')
            number_of_shares = data.get('requestObj', {}).get('number_of_shares')

            if not share_amount:
                return Response({'success': False, 'error': 'Share amount missing'}, status=400)

            share = Share.objects.create(
                amount=share_amount,
                user=user,
                transaction=transaction,
                number_of_shares=number_of_shares
            )

            # Get or create user's wallet and update balance
            user_wallet, created = UserWallet.objects.get_or_create(user=user)
            # print(f"User wallet before update: {user_wallet.balance}, Created: {created}")

            user_wallet.balance -= Decimal(share_amount)
            user_wallet.save()
            # print(user_wallet.balance)

            # Ensure there's only one saccos wallet, create if not exists
            saccos_wallet, saccos_wallet_created = SaccosWallet.objects.get_or_create(pk=1)
            if saccos_wallet_created:
                saccos_wallet.save()  # Ensure the initial instance is saved properly
            print(f"Saccos wallet before update: {saccos_wallet.balance}")

            saccos_wallet.balance += Decimal(share_amount)
            saccos_wallet.save()

            # send sms
            send_sms(user.phone_number, user.membership_number, transaction.description, share.amount)

            share_serializer = SharePaymentSerializer(share)
            transaction_serializer = TransactionSerializer(transaction)

            response = {
                'success': True,
                'share': share_serializer.data,
                'transaction': transaction_serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class AllShares(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shares = Share.objects.values('user').annotate(total_amount=Sum('amount')).order_by('-total_amount')
        total_shares = Share.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        user_share_data = []
        for share in shares:
            user = User.objects.get(id=share['user'])
            user_share_data.append({
                'name': user.name,
                'membership_number': user.membership_number,  
                'total_amount': share['total_amount'],
                'last_paid': Share.objects.filter(user=user).latest('date').date,
                'status': 'Active'  
            })

        response_data = {
            'success': True,
            'shares': user_share_data,
            'total_shares': total_shares
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    
class SavingPaymentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            print("User is authenticated:", user)
        else:
            print("User is not authenticated.")

        savings = Saving.objects.filter(user=user).order_by('-date')
        total_amount = savings.aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
        serializer = SavingPaymentSerializer(savings, many=True)

        response_data = {
            'success': True,
            "savings": serializer.data,
            "total_amount": total_amount
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data

            user_id = data.get('user', {}).get('id')
            if not user_id:
                return Response({'success': False, 'error': 'User data missing or invalid'}, status=400)
            
            user = get_object_or_404(User, id=user_id)

            transaction_data = data.get('successPaymentData', {})
                
            transaction = Transaction.objects.create(
                transaction_id=transaction_data.get('transaction_id'),
                created_at=transaction_data.get('created_at'),
                charge_response_code=transaction_data.get('charge_response_code'),
                amount=transaction_data.get('amount'),
                charged_amount=transaction_data.get('charged_amount'),
                description=transaction_data.get('description'),
                currency=transaction_data.get('currency'),
                tx_ref=transaction_data.get('tx_ref'),
                flw_ref=transaction_data.get('flw_ref'),
                status=transaction_data.get('status'),
                customer=user,
            )

            saving_amount = data.get('requestObj', {}).get('amount')

            if not saving_amount:
                return Response({'success': False, 'error': 'Saving amount missing'}, status=status.HTTP_400_BAD_REQUEST)

            saving = Saving.objects.create(
                amount=saving_amount,
                user=user,
                transaction=transaction
            )

            # Get or create user's wallet and update balance
            user_wallet, created = UserWallet.objects.get_or_create(user=user)
            print(f"User wallet before update: {user_wallet.balance}, Created: {created}")

            user_wallet.balance -= Decimal(saving_amount)
            user_wallet.save()
            print(user_wallet.balance)

            # Ensure there's only one saccos wallet, create if not exists
            saccos_wallet, saccos_wallet_created = SaccosWallet.objects.get_or_create(pk=1)
            if saccos_wallet_created:
                saccos_wallet.save()  # Ensure the initial instance is saved properly
            print(f"Saccos wallet before update: {saccos_wallet.balance}")

            saccos_wallet.balance += Decimal(saving_amount)
            saccos_wallet.save()

            # send sms
            send_sms(user.phone_number, user.membership_number, transaction.description, saving.amount)

            saving_serializer = SavingPaymentSerializer(saving)
            transaction_serializer = TransactionSerializer(transaction)

            response = {
                'success': True,
                'saving': saving_serializer.data,
                'transaction': transaction_serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AllSavings(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        savings = Saving.objects.values('user').annotate(total_amount=Sum('amount')).order_by('-total_amount')
        total_savings = Saving.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        user_saving_data = []
        for saving in savings:
            user = User.objects.get(id=saving['user'])
            user_saving_data.append({
                'name': user.name,
                'membership_number': user.membership_number,  
                'total_amount': saving['total_amount'],
                'last_paid': Saving.objects.filter(user=user).latest('date').date,
                'status': 'Active'  
            })

        response_data = {
            'success': True,
            'savings': user_saving_data,
            'total_savings': total_savings
        }
        return Response(response_data, status=status.HTTP_200_OK)


class EventListCreateRetrieveUpdateDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    model = Event
    serializer_class = EventSerializer
    user_model = User

    def get(self,request):
        events = self.model.objects.all()
        serializer = self.serializer_class(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if request.user.userType not in [6, 7]:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        user = request.user
        userr = self.user_model.objects.get(email=user)
        data['created_by'] = userr.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,event_id):
        event = self.model.objects.get(id=event_id)
        serializer = self.serializer_class(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, event_id):
        event = self.model.objects.get(id=event_id)
        event.delete()
        return Response({'message': 'Success'}, status=status.HTTP_200_OK)



class GenerateReportAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        month = request.data.get('month')
        year = request.data.get('year')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse(status=404)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Monthly_Report_{month}_{year}.pdf"'

        # Create PDF
        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        # Title
        p.setFont("Helvetica-Bold", 16)
        p.drawString(200, height - 50, f"Ripoti ya Mwezi {month}/{year}")

        # User Shares
        p.setFont("Helvetica-Bold", 12)
        p.drawString(30, height - 100, "Jumla ya Hisa: ")
        user_shares = Share.objects.filter(user=user, date__month=month, date__year=year).aggregate(Sum('amount'))
        p.drawString(150, height - 100, str(user_shares['amount__sum']))

        # User Savings
        p.drawString(30, height - 130, "Jumla ya Akiba: ")
        user_savings = Saving.objects.filter(user=user, date__month=month, date__year=year).aggregate(Sum('amount'))
        p.drawString(150, height - 130, str(user_savings['amount__sum']))

        # Events
        p.drawString(30, height - 160, "Matukio: ")
        events = Event.objects.filter(event_date__month=month, event_date__year=year)
        y_position = height - 190
        for event in events:
            p.drawString(50, y_position, f"{event.description} on {event.event_date.strftime('%d/%m/%Y')}")
            y_position -= 20

        # Loans
        p.drawString(30, y_position - 30, "Loans:")
        loans = Loan.objects.filter(user=user, loanRequestDate__month=month, loanRequestDate__year=year)
        y_position -= 60
        for loan in loans:
            p.drawString(50, y_position, f"Amount: {loan.loanRequestAmount}, Status: {loan.loanStatus}")
            y_position -= 20

        p.showPage()
        p.save()
        return response

    


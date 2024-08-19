from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from payment_sys.serializers import TransactionSerializer
from rest_framework import status
from .models import *
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from saccos_sys.models import Share, Saving
from loan_sys.models import Loan
from user_management.models import User
from django.db.models import Sum

# Create your views here.
class TransactionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        # Extract customer details
        customer_data = data.get('customer')
        customer, created = User.objects.get_or_create(
            email=customer_data['email'],
            defaults={
                'name': customer_data['name'],
                'phone_number': customer_data['phone_number'],
                'is_active': True,
            }
        )

        # If the customer already exists, update their attributes
        if not created:
            customer.name = customer_data['name']
            customer.phone_number = customer_data['phone_number']
            customer.is_active = True
            customer.userType = User.USER
            customer.save()


        # Extract transaction details
        transaction_data = {
            'transaction_id': data['transaction_id'],
            'created_at': data['created_at'],
            'charge_response_code': data['charge_response_code'],
            'amount': data['amount'],
            'charged_amount': data['charged_amount'],
            'currency': data['currency'],
            'description': data['description'],
            'tx_ref': data['tx_ref'],
            'flw_ref': data['flw_ref'],
            'status': data['status'],
            'customer': customer.id,
        }

        serializer = TransactionSerializer(data=transaction_data)

        if serializer.is_valid():
            if serializer.is_valid():
                transaction = serializer.save()
                response = {
                    'data': serializer.data,
                    'success': True
                }
                return Response(response, status=status.HTTP_201_CREATED)

            print('Validation Errors:', serializer.errors)  # Print the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserKiingilioTransactionView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        try:
            # Fetch transactions for the specified user with description "kiingilio"
            transactions = Transaction.objects.filter(customer=user_id, description="kiingilio")
            print(transactions)
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"error": "Transactions not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TransactionHistoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    model = Transaction

    def get(self, request):
        try:
            user = request.user

            transactions = self.model.objects.filter(customer=user)
            serializer = self.serializer_class(transactions, many=True)
            response = {
                'transactions': serializer.data,
                'success': True
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)


class UserFinancialData(APIView):
    authentication_classes = [TokenAuthentication]
    user_model = User
    share_model = Share
    saving_model = Saving
    loan_model = Loan

    def get(self, request, user_id):
        user = self.user_model.objects.get(id=user_id)
        shares = self.share_model.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        savings = self.saving_model.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        pending_loans = self.loan_model.objects.filter(user=user, loanStatus='PENDING').aggregate(Sum('amount_remaining'))['amount_remaining__sum'] or 0

        return Response({
            'shares': shares,
            'savings': savings,
            'pendingLoans': pending_loans
        }, status=status.HTTP_200_OK)

        

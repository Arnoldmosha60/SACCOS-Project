from decimal import Decimal
from django.db.models import Sum 
from loan_sys.serializers import LoanSerializer
from .models import Loan, LoanVerification
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from user_management.models import User
from django.utils import timezone
from datetime import timedelta, datetime
from saccos_sys.models import Saving, Share
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from payment_sys.models import Transaction, UserWallet, SaccosWallet
from rest_framework.permissions import IsAuthenticated

def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = int(source_date.year + month / 12)
    month = month % 12 + 1
    day = min(source_date.day, [31,
                                29 if year % 4 == 0 and not year % 100 == 0 or year % 400 == 0 else 28,
                                31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
    return datetime(year, month, day)

# Create your views here.
# checking if user is eligible to aplly for loan
class CheckLoanApplicationEligibilityView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # get the authenticated user
        user = request.user
        if not user.is_authenticated:
            print("User is not authenticated.")

        now = timezone.now()
        three_months_ago = now - timedelta(days=90)

        try:
            # Check if the user has paid savings for at least 3 months
            savings_count = Saving.objects.filter(user=user, date__gte=three_months_ago).count()
            has_paid_savings = savings_count >= 3

            # Check if user has paid shares for atleast three months
            shares_count = Share.objects.filter(user=user, date__gte=three_months_ago).count()
            has_paid_shares = shares_count >= 3

            # Check if user has less than three loans
            loans_count = Loan.objects.filter(user=user).count()
            has_few_loans = loans_count < 3

            if has_paid_savings and has_paid_shares and has_few_loans:
                return Response({'success': True}, status=status.HTTP_200_OK)
            return Response({'success': False, 'error': 'Not eligible'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'success': False, 'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


class LoanApplicationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    model = Loan
    serializer_class = LoanSerializer
    user_model = User

    def post(self, request):
        try:
            user = request.user

            pending_loans_count = self.model.objects.filter(user=user, loanStatus='PENDING').count()
            if pending_loans_count > 3:
                return Response({'success': False, 'message': "Max-limit"})

            # calculate loan_payment deadline date from loanRepayDuration
            loan_repay_duration = int(request.data.get('loanRepayDuration', 0))
            current_date = datetime.now()
            loan_payment_deadline = add_months(current_date, loan_repay_duration)
            print('+++++++++++++++++')
            print(request.data)

            loan_data = {
                'user': user.id,
                'loanType': request.data.get('loanType'),
                'loanRequestAmount': request.data.get('loanRequestAmount'),
                'loanDescription': request.data.get('loanDescription'),
                'referee': request.data.get('referee'),
                'loanRepayDuration': request.data.get('loanRepayDuration'),
                'loanRepayPerMonth': request.data.get('loanRepayPerMonth'),
                'loanRepaymentPlan': request.data.get('loanRepayType'),
                'loanPaymentDeadline': loan_payment_deadline,
            }

            serializer = self.serializer_class(data=loan_data)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save(user=user)
                response = {
                    'success': True,
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserPendingLoanList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LoanSerializer
    model = Loan

    def get(self, request):
        try:
            user = request.user

            pending_loans = self.model.objects.filter(user=user, loanStatus='PENDING')
            pending_loans = self.model.objects.filter(user=user, loanStatus='PENDING')
            serializer = self.serializer_class(pending_loans, many=True)

            response = {
                'success': True,
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class AllPendingLoansView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LoanSerializer
    model = Loan

    def get(self, request):
        try:
            pending_loans = self.model.objects.filter(loanStatus='PENDING')
            serializer = self.serializer_class(pending_loans, many=True)
            response = {
                'success': True,
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 


# check if the loan requested amount is eligible for allocation
class LoanVerificationView(APIView):
    authentication_classes = {TokenAuthentication}
    permission_classes = [IsAuthenticated]
    share_model = Share

    def post(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id)

        # Check if the loan type is 'Kujikimu'
        if loan.loanType == 'Kujikimu':
            return Response({'eligible': True})
        
        user_shares = self.share_model.objects.filter(user=loan.user).aggregate(total=Sum('amount'))['total'] or 0
        max_loan_amount = user_shares * 5

        # Check if request amount is eligible
        if loan.loanRequestAmount <= max_loan_amount:
            return Response({'eligible': True})
        return Response({'eligible': False})


class ApproveLoanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    model = LoanVerification

    def post(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id)
        is_valid = request.data.get('is_valid')
        reason = request.data.get('reason', '')
        transaction_data = request.data.get('successPaymentData', {})

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
                customer=request.user,
            )

        self.model.objects.create(
            loan=loan,
            is_verified=True,
            verification_reason=reason,
            verified_by=request.user,
            loan_verified_amount=transaction.charged_amount,
        )
        
        if is_valid == 'Eligible':
            loan.loanStatus = 'APPROVED'  
            loan.amount_remaining = transaction.amount
        else:
            loan.loanStatus = 'REJECTED' 
        loan.save()

        # Get or create user's wallet and update balance
        user_wallet, created = UserWallet.objects.get_or_create(user=loan.user)
        print(f"User wallet before update: {user_wallet.balance}, Created: {created}")

        user_wallet.balance += Decimal(transaction_data.get('charged_amount'))
        user_wallet.save()
        print(user_wallet.balance)

        # Ensure there's only one saccos wallet, create if not exists
        saccos_wallet, saccos_wallet_created = SaccosWallet.objects.get_or_create(pk=1)
        if saccos_wallet_created:
            saccos_wallet.save()  # Ensure the initial instance is saved properly
        print(f"Saccos wallet before update: {saccos_wallet.balance}")

        saccos_wallet.balance -= Decimal(transaction_data.get('charged_amount'))
        saccos_wallet.save()
        
        return Response({'success': True}, status=status.HTTP_200_OK)

    
    def put(self, request, loan_id):
        try:
            loan = Loan.objects.get(id=loan_id)
        except Loan.DoesNotExist:
            return Response({'success': False, 'message': 'Loan does not exist'}, status=status.HTTP_404_NOT_FOUND)

        amount_paid = request.data.get('amount')
        if not amount_paid:
            return Response({'success': False, 'message': 'Amount not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            amount_paid = Decimal(amount_paid)
        except ValueError:
            return Response({'success': False, 'message': 'Invalid amount format'}, status=status.HTTP_400_BAD_REQUEST)

        loan.amount_already_paid += amount_paid
        loan.amount_remaining -= amount_paid

        if loan.amount_remaining < 0:
            loan.amount_remaining = 0  # Prevent negative values
        
        loan.save()
        serializer = LoanSerializer(loan)

        transaction_data = request.data
        print(transaction_data)

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
            customer=request.user,
        )
        print(transaction)

        # Get or create user's wallet and update balance
        user_wallet, created = UserWallet.objects.get_or_create(user=loan.user)
        print(f"User wallet before update: {user_wallet.balance}, Created: {created}")

        user_wallet.balance -= Decimal(transaction.amount)
        user_wallet.save()
        print(user_wallet.balance)

        # Ensure there's only one saccos wallet, create if not exists
        saccos_wallet, saccos_wallet_created = SaccosWallet.objects.get_or_create(pk=1)
        if saccos_wallet_created:
            saccos_wallet.save()  # Ensure the initial instance is saved properly
        print(f"Saccos wallet before update: {saccos_wallet.balance}")

        saccos_wallet.balance += Decimal(transaction.amount)
        saccos_wallet.save()
        
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)



class UserApprovedLoanList(APIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = LoanSerializer
    model = Loan

    def get(self, request):
        try:
            user = request.user

            approved_loans = self.model.objects.filter(user=user, loanStatus='APPROVED')
            serializer = self.serializer_class(approved_loans, many=True)

            response = {
                'success': True,
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class GetLoanHistoryData(APIView):
    authentication_classes = [TokenAuthentication]
    loan_model = Loan
    loan_serializer = LoanSerializer
    loan_verification_model = LoanVerification

    def get(self, request):
        user = request.user
        loans = self.loan_model.objects.filter(user=user)
        loan_data = self.loan_serializer(loans, many=True).data
        return Response(loan_data, status=status.HTTP_200_OK)


class InstitutionLoansAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        loans = Loan.objects.filter(loanRepaymentPlan="makato ya mshahara")
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




    
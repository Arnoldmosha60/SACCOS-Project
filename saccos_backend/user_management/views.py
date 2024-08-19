import uuid
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from loan_sys.models import Loan
from loan_sys.serializers import LoanSerializer
from payment_sys.models import SaccosWallet, UserWallet
from saccos_sys.models import Event, Saving, Share
from saccos_sys.serializers import EventSerializer, SavingPaymentSerializer, SharePaymentSerializer
from user_management.serializers import ChangePasswordSerializer, UserProfileSerializer, UserSerializer
import requests
from requests.auth import HTTPBasicAuth
from django.contrib.auth import get_user_model
from rest_framework import generics
from payment_sys.serializers import SaccosWalletSerializer, TransactionSerializer
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from django.db.models import Sum

logger = logging.getLogger(__name__)
User = get_user_model()

def send_sms(phone_number, message):
    phone_number = phone_number

    # Prepare SMS data
    if phone_number.startswith('0'):
        phone_number = '255' + phone_number[1:]
    
    data = {
        "source_addr": "INFO",
        "schedule_time": "",
        "encoding": 0,
        "message": message,
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
class MembershipRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data.copy()
        transaction_data = user_data.pop('successPaymentData', None)

        # Create the user
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            print(user_serializer.errors)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the transaction
        if transaction_data:
            transaction_data['customer'] = user.id
            transaction_serializer = TransactionSerializer(data=transaction_data)

            if transaction_serializer.is_valid():
                transaction_serializer.save()

                 # Get or create user's wallet
                user_wallet, created = UserWallet.objects.get_or_create(user=user)

                # Get or create SaccosWallet (only create if it doesn't exist)
                saccos_wallet, saccos_wallet_created = SaccosWallet.objects.get_or_create(pk=1)  # Assuming id=1 for single instance
                if saccos_wallet_created:
                    saccos_wallet.save()  # Ensure the initial instance is saved properly

                # Update the wallets' balances
                try:
                    user_wallet.balance += transaction_data['charged_amount']
                    user_wallet.save()

                    saccos_wallet.balance += transaction_data['charged_amount']
                    saccos_wallet.save()

                except ValueError as e:
                    return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                response = {
                    'data': transaction_serializer.data,
                    'success': True
                }
                return Response(response, status=status.HTTP_201_CREATED)

            print('Validation Errors:', transaction_serializer.errors)  # Print the validation errors
            return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': False, 'error': 'No transaction data provided'}, status=status.HTTP_400_BAD_REQUEST)


class MembershipRequestListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get(request):
        users = User.objects.filter(userType=User.PENDING)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status =status.HTTP_200_OK)
    

class AdminVerifyMembershipRequestView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, user_id):
        try:
            # Fetch the user with PENDING status
            user = get_object_or_404(User, id=user_id, userType=User.PENDING)
            print(user)
        except User.DoesNotExist:
            return Response({'error': 'User not found or already verified'}, status=status.HTTP_404_NOT_FOUND)
        
        # Generate a random password
        password = get_random_string(length=10)
        print(password)
        
        # Update user details
        user.membership_number = request.data.get('membershipNumber')
        user.set_password(password)
        user.userType = User.USER
        user.is_active = True
        user.save()

        name = user.name
        phone_number = user.phone_number
        email = user.email
        membership_number = user.membership_number

        send_sms(
            phone_number,
            message=f"Habari {name}, maombi yako ya uanachama wa DIT SACCOS LTD yamekubaliwa kikamilifu na sasa wewe ni mwanachama wa kikundi hiki. Namba yako ya usjaili ni {membership_number} na nywila yako ni {password}. Jumuiya ya wanaSACCOS ya DIT tunakukaribisha",
        )

        return Response({'message': 'User created and SMS sent successfully'}, status=status.HTTP_201_CREATED)


# @method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                login(request, user)
                serializer = UserSerializer(user, context={'request': request})
                return Response({
                    'token': token.key,
                    'user': serializer.data,
                    'success': True,
                    'msg': 'Login Success'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Account is inactive'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserInformation(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get(request, query_type):
        if query_type == 'single':
            try:
                user_id = request.GET.get('user_id')
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'message': 'User Does Not Exist'}, status=404)
            serializer = UserSerializer(instance=user, many=False, context={'request': request})
            return Response(serializer.data)

        elif query_type == 'all':
            # 1 for ADMIN, 2 for USER
            queryset = User.objects.filter(userType__in=[2,4,5,6,7])  
            # Log user IDs
            logger.debug(f"Queryset: {[user.id for user in queryset]}")  
            serializer = UserSerializer(instance=queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif query_type == 'current':
            user = request.user
            serializer = UserSerializer(instance=user, many=False, context={'request': request})
            return Response({'success': True, 'user': serializer.data})

        elif query_type == 'users':
            queryset = User.objects.filter(is_staff=False)  # Filtering system users
            serializer = UserSerializer(instance=queryset, many=True, context={'request': request})
            return Response(serializer.data)

        else:
            return Response({'message': 'Wrong Request!'}, status=400)


class SearchUserView(APIView):
    authentication_classes = [TokenAuthentication]
    model = User
    serializer_class = UserSerializer

    def get(self, request):
        query = request.GET.get('query', '')
        print('+++++++++++++++++++')
        print(query)

        if query:
            users = User.objects.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(membership_number__icontains=query)
            )
            if users.exists(): 
                serializer = self.serializer_class(users, many=True)
                return Response({
                    'success': True,
                    'msg': 'User Found',
                    'users': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'No users found with the given query'})
        else:
            user = self.model.objects.all()
            serializer = self.serializer_class(user, many=True)
            return Response({
                'msg': 'All Users',
                'users': serializer.data
            }, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request):
        user = request.user
        data = request.data.copy()

        # Check if a profile picture is included in the request
        if 'profile' in request.FILES:
            data['profile'] = request.FILES['profile']
            print(data['profile'])
        
        serializer = UserProfileSerializer(user, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            response = {
                'data': serializer.data,
                'success': True
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    lookup_field = 'pk'

    def get_object(self):
        # Override get_object to fetch user based on the provided pk
        return User.objects.get(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check old password
        if not user.check_password(serializer.data.get("currentPassword")):
            return Response({"currentPassword": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(serializer.data.get("newPassword"))
        user.save()

        return Response({"detail": "Password updated successfully"})


class DeleteMember(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    model = User
    saccos_wallet_model = SaccosWallet

    def delete(self, request, user_id, format=None):
        try:
            user = self.model.objects.get(id=user_id)

            phone_number = user.phone_number

            send_sms(
                user.phone_number,
                message=f"Habari {user.name}, Uongozi wa DIT SACCOS LIMITED umefikia muafaka wa kukuondoa uanachama",
            )
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateUserRole(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    model = User
    serializer = UserSerializer

    def put(self, request, user_id):
        try:
            user = self.model.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        user.userType = data.get('userType', user.userType)
        user.save()
        return Response({"message": "User role updated successfully"}, status=status.HTTP_200_OK)


class RestrictUserView(APIView):
    authentication_classes = [TokenAuthentication]
    model = User

    def put(self, request, user_id):
        try: 
            user = self.model.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        reason = request.data.get('reason', '')
        user.is_active = False
        user.save()

        send_sms(
                user.phone_number,
                message=f"Habari {user.name}, Uongozi wa DIT SACCOS LIMITED umefikia muafaka wa kusitisha uanachama wako sababu ni {reason}",
            )
        
        return Response({'message': 'User status updated successfully'}, status=status.HTTP_200_OK)


class ReturnUserMembershipView(APIView):
    authentication_classes = [TokenAuthentication]
    model = User

    def put(self, request, user_id):
        try:
            user = self.model.objects.get(id=user_id)
        except self.model.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = True
        user.save()

        send_sms(
                user.phone_number,
                message=f"Habari {user.name}, Uongozi wa DIT SACCOS LIMITED umefikia muafaka wa kurudisha uanachama wako.",
            )
        return Response({'message': 'User status updated successfully'}, status=status.HTTP_200_OK)


class UserDashboardInformation(APIView):
    # authentication_classes = [TokenAuthentication]
    user_wallet_model = UserWallet
    share_model = Share
    saving_model = Saving
    user_model = User
    loan_model = Loan
    events_model = Event

    def get(self, request, user_id):
        user = self.user_model.objects.get(id=user_id)
        user_wallet = self.user_wallet_model.objects.filter(user=user).first()
        shares = self.share_model.objects.filter(user=user)
        savings = self.saving_model.objects.filter(user=user)
        loans = self.loan_model.objects.filter(user=user)
        events = self.events_model.objects.all().count()

        total_shares_amount = shares.aggregate(total=Sum('amount'))['total'] or 0
        total_savings_amount = savings.aggregate(total=Sum('amount'))['total'] or 0
        total_loans_amount = loans.aggregate(total=Sum('loanRequestAmount'))['total'] or 0
        total_users = self.user_model.objects.all().count()

        user_wallet_balance = user_wallet.balance if user_wallet else 0

        return Response({
            'user_wallet_balance': user_wallet_balance,
            'shares': total_shares_amount,
            'savings': total_savings_amount,
            'loans': total_loans_amount,
            'events': events,
            'total_users': total_users,
        }, status=status.HTTP_200_OK)


class GeneralDashboardInformation(APIView):
    permission_classes = [AllowAny]
    saccos_wallet_model = SaccosWallet
    share_model = Share
    saving_model = Saving
    user_model = User
    loan_model = Loan
    events_model = Event

    def get(self, request):
        saccos_wallet = self.saccos_wallet_model.objects.all()
        shares = self.share_model.objects.all()
        savings = self.saving_model.objects.all()
        loans = self.loan_model.objects.all()
        events = self.events_model.objects.all().count()

        total_shares_amount = shares.aggregate(total=Sum('amount'))['total'] or 0
        total_savings_amount = savings.aggregate(total=Sum('amount'))['total'] or 0
        total_loans_amount = loans.aggregate(total=Sum('loanRequestAmount'))['total'] or 0
        total_users = self.user_model.objects.all().count()

        # Extracting balance from the first entry in saccos_wallet queryset
        sacco_balance = saccos_wallet.first().balance if saccos_wallet.exists() else 0

        return Response({
            'saccos_wallet_balance': sacco_balance,
            'shares': total_shares_amount,
            'savings': total_savings_amount,
            'loans': total_loans_amount,
            'events': events,
            'total_users': total_users
        }, status=status.HTTP_200_OK)


        
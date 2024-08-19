from django.urls import path
from user_management.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'user_management'

urlpatterns = [
    path('login', LoginView.as_view()),
    path('get-users/<str:query_type>/', UserInformation.as_view(), name="get-users"),
    path('change-password/<uuid:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('delete-user/<uuid:user_id>/', DeleteMember.as_view(), name='delete_user'),
    path('update-user-role/<uuid:user_id>/', UpdateUserRole.as_view(), name='update_user_role'),
    path('restrict-user/<uuid:user_id>/', RestrictUserView.as_view(), name='restrict_user'),
    path('return-user-membership/<uuid:user_id>/', ReturnUserMembershipView.as_view(), name='return_user_membership'),
    path('search-user/', SearchUserView.as_view(), name='search_user'),

    path('membership-request', MembershipRequestView.as_view(), name="membership_request"),
    path('membership-requests-list', MembershipRequestListView.as_view(), name='membership-request-list'),
    path('admin-verify-membership-request/<uuid:user_id>/', AdminVerifyMembershipRequestView.as_view(), name='create-user-from-membership-request'),

    path('user-information/<uuid:user_id>/', UserDashboardInformation.as_view(), name='get_user_information'),
    path('general-information/', GeneralDashboardInformation.as_view(), name="general_information"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
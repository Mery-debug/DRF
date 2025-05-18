from django.urls import path

from users.apps import UsersConfig
from users.views import (
    PaymentListAPIView,
    UsersListAPIView,
    UsersCreateAPIView,
    UsersDestroyAPIView,
    UsersUpdateAPIView,
    MembershipCreateAPIView, PaymentsCreateAPIView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('list/', UsersListAPIView.as_view(), name='user_list'),
    path('register/', UsersCreateAPIView.as_view(), name='register'),
    path('update/', UsersUpdateAPIView.as_view(), name='user_update'),
    path('delete/', UsersDestroyAPIView.as_view(), name='user_delete'),
    path('create_member/', MembershipCreateAPIView.as_view(), name='create_member'),
    path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments-create'),
]

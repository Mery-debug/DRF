from rest_framework.decorators import permission_classes, api_view
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, TokenSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenSerializer


@permission_classes([AllowAny])
class UsersCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


@permission_classes([IsAuthenticated])
class UsersListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@permission_classes([IsAuthenticated])
class UsersRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@permission_classes([IsAuthenticated])
class UsersUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@permission_classes([IsAuthenticated])
class UsersDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('pay_course', 'pay_lesson', 'variation_cost')
    ordering_fields = ('date_payment',)


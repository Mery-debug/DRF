from rest_framework.decorators import permission_classes, api_view
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
class UsersListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
class UsersRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
class UsersUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
class UsersDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('pay_course', 'pay_lesson', 'variation_cost')
    ordering_fields = ('date_payment',)


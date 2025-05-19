from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from lms.models import Course
from lms.serializers import MembershipSerializer
from lms.services import create_price, create_stripe_product, create_stripe
from users.api_errors import ServiceUnavailable, custom_exception_handler
from users.models import Payment, User, Membership
from users.serializers import PaymentSerializer, UserSerializer, TokenSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenSerializer


class UsersCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

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


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    exception_handler = custom_exception_handler

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = payment.pay_course or payment.pay_lesson
        product = create_stripe_product(product.name)
        price = create_price(product.id, payment.total_cost)
        session = create_stripe(price.id)
        payment.payment_session_id = session.id
        payment.payment_link = session.url
        payment.save()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('pay_course', 'pay_lesson', 'variation_cost')
    ordering_fields = ('date_payment',)


class MembershipCreateAPIView(generics.CreateAPIView):
    serializer_class = MembershipSerializer
    queryset = Membership.objects.all()

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Membership.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Membership.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
        return Response({"message": message})

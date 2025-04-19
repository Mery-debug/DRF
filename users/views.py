from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics

from users.models import Payment
from users.serializers import PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('pay_course', 'pay_lesson', 'variation_cost')
    ordering_fields = ('date_payment',)


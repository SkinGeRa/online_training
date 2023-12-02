import os

import stripe
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from payments.models import Payment
from payments.serializers import PaymentsSerializer
from payments.services import create_payment


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('lesson', 'course', 'payment_method',)
    ordering_fields = ('payment_date',)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payment.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data.get('amount')
        user = self.request.user
        payment = create_payment(amount, user)
        response_data = {
            "id": payment.id,
            "payment_amount": payment.amount
        }
        headers = self.get_success_headers(serializer.data)

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer

    def get(self, request, pk):
        try:
            payment = get_object_or_404(Payment, pk=pk)
            stripe_id = payment.stripe_id
            stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
            payment_intent = stripe.PaymentIntent.retrieve(stripe_id)

            return Response(payment_intent, status=status.HTTP_200_OK)

        except Payment.DoesNotExist:
            return Response({"error": "Платеж не найден"}, status=status.HTTP_404_NOT_FOUND)
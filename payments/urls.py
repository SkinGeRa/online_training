from django.urls import path

from payments.apps import PaymentsConfig
from payments.views import PaymentsListAPIView, PaymentCreateAPIView, PaymentRetrieveAPIView

app_name = PaymentsConfig.name

urlpatterns = [
    path('', PaymentsListAPIView.as_view(), name='payment_list'),
    path('create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('retrieve/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_retrieve')
]
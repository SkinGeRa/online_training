from rest_framework import serializers

from payments.models import Payment


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

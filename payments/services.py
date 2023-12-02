import os
import stripe

from payments.models import Payment


def create_payment(amount, user):
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
        payment_method_types=['card'],
        description=f'Payment for {user}',
    )

    payment = Payment.objects.create(
        user=user,
        amount=amount,
        stripe_id=payment_intent.id
    )

    return payment


def retrieve(stripe_id):
    return stripe.PaymentIntent.retrieve(stripe_id)
from django.shortcuts import render
from rest_framework.response import Response
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status
import stripe
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

# class StripeCheckoutView
@api_view(['POST'])
def test_payment(request):
    print('heiii')
    test_payment_intent = stripe.PaymentIntent.create(
    amount=1000, currency='pln', 
    payment_method_types=['card'],
    receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)
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
    amount=200000000, currency='inr', 
    payment_method_types=['card'],
    receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)

@api_view(['POST'])
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            print("create checkout session.......")
            # Create a Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                # billing_details={
                #     "name": "nandu",
                #     "email":"nandu.ganesh.nair@gmail.com",
                #     "phone":"+919805464357",
                #     "address": {
                #     "line1": "123 Main St",
                #     "city": "Thalassery",
                #     "state": "Kerala",
                #     "postal_code": "670741",
                #     "country": "IN",
                #     },
                # },
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'Slot Booking',
                        },
                        'unit_amount': 250000,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:5173',
                cancel_url='http://localhost:5173/student/profile',
            )
            return Response({'id': checkout_session.id})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


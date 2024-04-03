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
            
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'SLOTS AVAILABLE',
                            "description": "Book a slot for your private session now. ",
                            "images" : ["http://localhost:8000/media/Images/pexels-pixabay-159866.jpg"]
                        },
                        'unit_amount': 250000,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                billing_address_collection= 'required',
                success_url='http://localhost:5173/student/paymentSuccess',
                cancel_url='http://localhost:5173/student/profile',
            )
            return Response({'id': checkout_session.id})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


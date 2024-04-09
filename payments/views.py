from django.shortcuts import render
from Scheduler.models import Booking
from .serializers import BookingSerializer
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

            serializer = BookingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            booking_data = serializer.validated_data
            
            user_id = booking_data.get('booked_by')
            slot_id = booking_data.get('slot')

            # booking =Booking.objects.create(booked_by=user_id, slot=slot_id)

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
                metadata={
                    'user_id':user_id,
                    'slot_id':slot_id,
                }
            )
            return Response({'id': checkout_session.id})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@api_view(['POST'])
def stripe_webhook(request):
    print('webhook')
    # print('Received webhook request:', request.body)
    # print('Received headers:', request.headers)
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print(stripe.api_key)
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        print('valueerror')
        return Response({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('signatureVerificationError')
        return Response({'error': str(e)}, status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Process the payment_intent here
        handle_payment_intent_succeeded(payment_intent)

    return Response({'success': True})

def handle_payment_intent_succeeded(payment_intent):
    # Extract payment-related information
    print('handling payment success')
    amount = payment_intent['amount']
    currency = payment_intent['currency']
    customer_email = payment_intent['charges']['data'][0]['billing_details']['email']
    
    # Extract metadata
    metadata = payment_intent['metadata']
    slot_id = metadata.get('slot_id')
    user_id = metadata.get('user_id')
    
    # Save the information to your database
    # For example, create a new Booking model instance
    Booking.objects.create(
        amount=amount,
        currency=currency,
        slot=slot_id,
        booked_by=user_id,

    )
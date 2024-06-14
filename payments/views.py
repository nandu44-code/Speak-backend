from django.shortcuts import render
from Scheduler.models import Booking,Slots
from Users.models import CustomUser
from .serializers import BookingSerializer
from rest_framework.response import Response
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework import status
import stripe
import os
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
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
            print('serializer is working properly ')
            
            if not serializer.is_valid():
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            print('serializer is validated properly')
            booking_data = serializer.validated_data
            
            user_id = booking_data.get('booked_by').id
            slot_id = booking_data.get('slot').id

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'SLOTS AVAILABLE',
                            'description': 'Book a slot for your private session now.',
                            'images': ['http://localhost:8000/media/Images/pexels-pixabay-159866.jpg']
                        },
                        'unit_amount': 250000,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                billing_address_collection='required',
                success_url='http://localhost:5173/student/paymentSuccess',
                cancel_url='http://localhost:5173/student/profile',
                payment_intent_data={
                    'metadata': {
                        'user_id': user_id,
                        'slot_id': slot_id,
                    }
                }
            )
            return Response({'id': checkout_session.id})
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def stripe_webhook(request):
    print('webhook')
    print(stripe_webhook_secret)
    # print('Received webhook request:', request.body)
    # print('Received headers:', request.headers)
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print(stripe.api_key)
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        print('value error')
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
    print(payment_intent)
    amount = payment_intent['amount']
    currency = payment_intent['currency']
    # customer_email = payment_intent['charges']['data'][0]['billing_details']['email']
    
    # Extract metadata
    metadata = payment_intent['metadata']
    slot_id = metadata.get('slot_id')
    user_id = metadata.get('user_id')
    print(slot_id)
    print(user_id)
    slot_instance = Slots.objects.get(id=slot_id)
    if slot_instance:
        slot_instance.is_booked = True
        slot_instance.save()
    user_instance = CustomUser.objects.get(id=user_id)
    # Save the information to your database
    # For example, create a new Booking model instance
    

    Booking.objects.create(
        amount=amount,
        currency=currency,
        slot=slot_instance,
        booked_by=user_instance,  

    )
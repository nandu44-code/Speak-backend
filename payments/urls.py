from django.urls import path
from payments import views

urlpatterns =[
   path('test-payment/', views.test_payment),
   path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
]

import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():

    otp = random.randint(100000,999999)
    return otp

def send_otp(email,otp):
    print('send_otp function')
    subject = "Your OTP for registration at speak"
    message = f"Your otp is {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [ email ]   

    send_mail(subject, message, from_email, recipient_list)
    
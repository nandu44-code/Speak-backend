from django.core.mail import send_mail
from django.conf import settings

def send_otp(email,otp):
    subject = "Your OTP for registration at speak"
    message = f"Your otp is {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [ email ]   

    send_mail(subject, message, from_email, recipient_list)
    
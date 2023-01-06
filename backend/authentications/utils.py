from django.core.mail import EmailMessage
from django.conf import settings 

class RegisterEmailNotification:
    @staticmethod
    def send_email_notification(domain_name, user, token, abs_path):
        subject = f"ACCOUNT VERIFICATION"
        absurl = 'http://'+domain_name+abs_path+'?token='+str(token)
        message = f"Hi {user.first_name}, \n Kindly use below link to activate your email \n {absurl}"
        email = EmailMessage(subject=subject,body=message,to=[user.email])
        email.send()

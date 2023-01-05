from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings 

class RegisterEmailNotification:
    '''
    Register email notification class
    '''
    def __init__(self, domain_name, user, token):
        self.domain_name = domain_name
        self.user = user
        self.token = token 
    
    def get_message_subject(self):
        return f"ACCOUNT VERIFICATION"
    
    def get_message_body(self):
        abs_path = reverse('verify_email')
        print("abs",abs_path)
        absurl = 'http://'+self.domain_name+abs_path+'?token='+str(self.token)
        print("urls",absurl)
        message = f"Hi {self.user.first_name}, \n Kindly use below link to activate your email \n {absurl}"
        print(message)
        return message
    
    def send_email_notification(self):
        email = EmailMessage(subject=self.get_message_subject, body=self.get_message_body, from_email=settings.EMAIL_HOST_USER, to=[self.user.email])
        email.send(fail_silently=True)
        return True
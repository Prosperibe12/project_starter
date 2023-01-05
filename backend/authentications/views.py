from django.contrib.sites.shortcuts import get_current_site 

from rest_framework import generics
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken

from backend import utils 
from backend.authentications import serializers
from backend import models 
from backend.authentications.utils import RegisterEmailNotification

class RegisterView(generics.GenericAPIView):
    '''
    A class that registers a new User
    '''
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.RegisterSerializer
    
    def post(self, request):
        data = request.data 
        serializer_data = self.serializer_class(data=data)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            
            # send email notification and link for account activation
            domain_name = get_current_site(request).domain
            user = models.User.objects.get(email=serializer_data.data['email'])
            token = RefreshToken.for_user(user).access_token
            email_message = RegisterEmailNotification(domain_name, user, token).send_email_notification()
            if email_message:
                return utils.CustomResponse.Success(serializer_data.data, status=status.HTTP_201_CREATED)
        return utils.CustomResponse.Failure(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmail(generics.GenericAPIView):
    
    authentication_classes = ()
    permission_classes = ()
    
    def get(self, request):
        pass 
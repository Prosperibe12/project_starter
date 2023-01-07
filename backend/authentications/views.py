from django.contrib.sites.shortcuts import get_current_site 
from django.urls import reverse
from django.conf import settings

from rest_framework import generics
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

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
            abs_path = reverse('verify-email')
            user = models.User.objects.get(email=serializer_data.data['email'])
            token = RefreshToken.for_user(user).access_token
            RegisterEmailNotification().send_email_notification(domain_name, user, token,abs_path)
            return utils.CustomResponse.Success(serializer_data.data, status=status.HTTP_201_CREATED)
        return utils.CustomResponse.Failure(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmail(generics.GenericAPIView):
    '''
    A view that verifies a user email and set user.is_verified attribute to True
    '''
    authentication_classes = ()
    permission_classes = ()
    
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = models.User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return utils.CustomResponse.Success("Successfully Activated", status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            return utils.CustomResponse.Failure("Activation Link Expired", status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError as e:
            return utils.CustomResponse.Failure("Invalid Token", status=status.HTTP_400_BAD_REQUEST)
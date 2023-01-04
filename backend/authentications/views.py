from rest_framework import generics
from rest_framework import status 

from backend import utils 
from backend.authentications import serializers
from backend import models 

class RegisterView(generics.GenericAPIView):
    '''
    A class that registers a new user
    '''
    authentication_classes = ()
    serializer_class = serializers.RegisterSerializer
    
    def post(self, request):
        data = request.data 
        serializer_data = self.serializer_class(data=data)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            return utils.CustomResponse.Success(serializer_data.data, status=status.HTTP_201_CREATED)
        return utils.CustomResponse.Failure(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
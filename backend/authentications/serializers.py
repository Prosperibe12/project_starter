from rest_framework import serializers 

from backend import models 

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = models.User 
        fields = ['id','first_name','last_name','email','password']
        
    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)
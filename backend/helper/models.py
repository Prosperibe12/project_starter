from django.db import models 

class HelperModel(models.Model):
    '''
    Custom Helper Model
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
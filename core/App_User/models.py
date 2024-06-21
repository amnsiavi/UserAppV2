from django.db import models
from datetime import datetime

# Create your models here.
class UserAppModel(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    website = models.URLField()
    address = models.JSONField(default=dict(
        street='', suite = '', city = '',
        zip_code = '', geo_location={'lat':0.0,'lng':0.0},
        
    ))
    company = models.JSONField(default=dict(
        name='', catchPhrase='',bs=''
    ))
    created = models.DateTimeField(default=datetime.now())
    updated = models.DateTimeField(default=datetime.now())
    
    
    def __str__(self):
        return self.name
    
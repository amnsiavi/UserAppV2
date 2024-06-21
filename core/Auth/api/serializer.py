from rest_framework.serializers import ModelSerializer

# User Authentication Model
from django.contrib.auth.models import User



class AuthSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','username','email','password','is_superuser']
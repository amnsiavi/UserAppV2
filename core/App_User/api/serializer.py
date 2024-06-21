from rest_framework.serializers import ModelSerializer, SerializerMethodField
from App_User.models import UserAppModel
from datetime import datetime
class AppUserSerializer(ModelSerializer):
    
    created_at = SerializerMethodField()
    updated_at = SerializerMethodField()
    
    class Meta:
        model = UserAppModel
        exclude = ['created','updated']
    
    def get_created_at(self,object):
        return object.created.strftime('%Y-%m-%d-%H:%M:%S')
    
    def get_updated_at(self,object):
        return object.updated.strftime('%Y-%m-%d-%H:%M:%S')    
    
    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email',instance.email)
        instance.address = validated_data.get('address',instance.address)
        instance.phone = validated_data.get('phone',instance.phone)
        instance.website = validated_data.get('website',instance.website)
        instance.company = validated_data.get('company',instance.company)
        
        instance.update = datetime.now()
        instance.save()
        return instance
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import User_Profile, MenuItem

class User_ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Profile
        fields = ('user.username', 'gcm_id', 'fb_id')
        
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
from dataclasses import fields
from rest_framework import serializers
from GlobalApi.models import User, Client, Admin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['doc']
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

#Information serializers are the one that shows specific information to put on another serializer
class ClientInformationSerializer(serializers.ModelSerializer):
    
    doc_client = UserInformationSerializer(read_only = True)
    
    class Meta:
        model = Client
        fields = ['id_client', 'doc_client' ,'name_client', 'last_name_client','email_client']
        
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
                


from dataclasses import fields
from rest_framework import serializers
from GlobalApi.models import User, Client

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    #Override the method create in the serializer to hash the password
    def create(self, validated_data):
        user_hashed = User(**validated_data)
        #set_password is a method that comes with the User model, it hashes the password so the client can log in
        user_hashed.set_password(validated_data['password'])
        user_hashed.save()
        return user_hashed

    #Override the method update in the serializer to hash the password
    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user

        
class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['doc']

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('doc', 'username')
        
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
        



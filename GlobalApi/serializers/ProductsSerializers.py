from dataclasses import fields
from rest_framework import serializers
from GlobalApi.models import User, Products, Client, ProductUnits

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        

class ProductUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnits
        fields = '__all__'
        
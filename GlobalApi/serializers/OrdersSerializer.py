from dataclasses import fields
from rest_framework import serializers
from GlobalApi.models import Order
from GlobalApi.serializers.UsersSerializer import ClientInformationSerializer
from GlobalApi.serializers.ProductsSerializer import ProductUnitsListSerializer

#Normal serializers for the views
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
#ListSerializers are the ones that show information in the front
class ListOrderSerializer(serializers.ModelSerializer):
    
    order_client_id =  ClientInformationSerializer(many=False)
    order_product_units = ProductUnitsListSerializer(many = True)
    
    class Meta:
        model = Order
        fields = ['order_id','order_client_id','order_address','order_date','order_product_units','order_state']
    
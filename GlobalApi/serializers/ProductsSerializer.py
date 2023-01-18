from dataclasses import fields
from rest_framework import serializers
from GlobalApi.models import Products, ProductUnits
from GlobalApi.serializers.CategoriesSerializer import CategoriesSerializer


# Product Serializers for the creation of the product and the update of the product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        
#This serializer will be shown in the ProductUnitsListSerializer
class ProductListSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Products
        fields = ['product_id','name','description','price','image', 'category' ,'available']


# Product Serializer with Stock from the ProductUnits
# This serializer will show the information of the product in the main page, with the full information, even the stock
class ProductsWithStockUnitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ['product_id','name','description','price','image', 'category' ,'available', 'stock']


# Product Units Serializers for the creation of the product units and the update of the product units

class ProductUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnits
        fields = '__all__'


#This serializer will show the information of the product in the Order, will not show the Stock
class ProductUnitsListSerializer(serializers.ModelSerializer):

    product_id = ProductListSerializer(read_only=True)

    class Meta:
        model = ProductUnits
        fields = ['product_unit_id', 'product_id' ,'product_unit_state']
        


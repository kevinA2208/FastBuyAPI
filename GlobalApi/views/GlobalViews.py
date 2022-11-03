from rest_framework import viewsets
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import User, Products
from GlobalApi.serializers.serializers import UserSerializer, ProductSerializer

class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    def get_queryset(self, doc=None):
        if doc == None:
            return User.objects.all()
        return User.objects.get(doc=doc)
        
class ProductViewSet(viewsets.ViewSet):
    serializer_class = ProductSerializer
    def get_queryset(self, id=None):
        if id == None:
            return Products.objects.all()
        return Products.objects.get(id=id)

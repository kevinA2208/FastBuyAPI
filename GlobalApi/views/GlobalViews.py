from rest_framework import viewsets
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import User, Products
from GlobalApi.serializers.ProductsSerializers import ProductSerializer
from GlobalApi.serializers.UsersSerializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self, doc=None):
        if doc == None:
            return User.objects.all()
        return User.objects.get(doc=doc)
        






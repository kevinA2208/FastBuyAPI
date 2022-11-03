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
        return Products.objects.get(id=id).first()

    def create(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serialize.save()
            message = "The product ${serializer.data.name} has been created succesfuly!"
            return Response({'data' : serializer.data, 'message' : message}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def update(self, request, id):
        product = Products.objects.filter(id=id).first()
        serializer = ProductSerializer(product, data = request.data)
        if serializer.is_valid():
            serializer.save()
            message = "The product ${serializer.data.name} has been updated succesfuly!"
            return Response({'data' : serializer.data, 'message': message}, status = status.HTTP_200_OK)
        return Responde(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, id):
        product = Products.objects.filter(id=id).first()
        product.delete()
        message = "The product has been deleted succesfuly!"
        return Response({'message': message}, status = status.HTTP_200_OK)
    





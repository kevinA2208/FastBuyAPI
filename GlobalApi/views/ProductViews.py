from rest_framework import viewsets
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Products
from GlobalApi.serializers.ProductsSerializers import ProductSerializer



class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    def get_queryset(self, pk=None):
        if pk == None:
            return Products.objects.all()
        return Products.objects.filter(product_id = pk).first()

    #To create the product the stock needs to be above 0
    def create(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            if int(request.data["stock"]) <= 0:
                message = "The stock of the product can't be 0 or less!"
                return Response({'message':message}, status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            message = "The product has been created succesfuly!"
            return Response({'data' : serializer.data, 'message' : message}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    #To update the product the stock can be 0 but it will not be available, cant be less than 0
    def update(self, request, pk):
        product = Products.objects.filter(product_id=pk).first()
        serializer = ProductSerializer(product, data = request.data)
        if serializer.is_valid():
            #If the stock is 0, the client can't buy that product
            if int(request.data['stock']) == 0:
                serializer.validated_data['available'] = False
                serializer.save()
                message = "The product has been updated succesfuly!"
                return Response({'data' : serializer.data, 'message': message}, status = status.HTTP_200_OK)
            if int(request.data['stock']) < 0:
                message = "The stock of the product can't be less than 0!"
                return Response({'message':message}, status = status.HTTP_400_BAD_REQUEST)
            serializer.validated_data['available'] = True
            serializer.save()
            message = "The product has been updated succesfuly!"
            return Response({'data' : serializer.data, 'message': message}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        product = Products.objects.filter(product_id=pk).first()
        product.delete()
        message = "The product has been deleted succesfuly!"
        return Response({'message': message}, status = status.HTTP_200_OK)
    
from rest_framework import viewsets
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Products, ProductUnits
from GlobalApi.serializers.ProductsSerializer import ProductSerializer, ProductsWithStockUnitsSerializer, ProductUnitsSerializer
from datetime import timedelta, date
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler({'apscheduler.job_defaults.max_instances': 1})

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    def get_queryset(self, pk=None):
        if pk == None:
            return Products.objects.all()
        return Products.objects.filter(product_id = pk).first()


    def create(self, request):

        data = request.data
        serializer_product = ProductsWithStockUnitsSerializer(data = data)
        if serializer_product.is_valid():
            stock = serializer_product.validated_data.get('stock')
            #If stock is less or equal to 0, the product doesnt create
            if(stock <= 0):
                message = "The stock can't be 0 or less"
                return Response({'message' : message}, status = status.HTTP_400_BAD_REQUEST)
            #If stock is greater than 0, the product will be created and the product units from the stock too
            elif (stock > 0):
                saved_product = serializer_product.save()
                message = "The product and the product units has been created succesfuly!"
                #For every stock, a product unit will be created
                for item in range(stock):
                    #The product unit state will be A for available
                    product_unit_serializer = ProductUnits(product_id = saved_product, product_unit_state = "A") 
                    product_unit_serializer.save()
                return Response({'data' : serializer_product.data, 'message' : message}, status = status.HTTP_201_CREATED)
        return Response(serializer_product.errors, status= status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        product = Products.objects.filter(product_id=pk).first()
        serializer_product = ProductSerializer(product, data = request.data)
        if serializer_product.is_valid():
            stock = serializer_product.validated_data.get('stock')
            previous_stock = product.stock
            if(stock < previous_stock):
                message = "The stock can't be less than the previous stock"
                return Response({'message' : message}, status = status.HTTP_400_BAD_REQUEST)
            elif(stock > previous_stock):
                for item in range(stock - previous_stock):
                    product_unit_serializer = ProductUnits(product_id = product, product_unit_state = "A") 
                    product_unit_serializer.save()
                serializer_product.save()
                message = "The product and the stock has been updated succesfuly!"
                return Response({'data' : serializer_product.data, 'message': message}, status = status.HTTP_200_OK)
            elif(stock == previous_stock):
                serializer_product.save()
                message = "The product has been updated succesfuly!"
                return Response({'data' : serializer_product.data, 'message': message}, status = status.HTTP_200_OK)

        return Response(serializer_product.errors, status = status.HTTP_400_BAD_REQUEST)
    
    #Delete the product and the product units
    def destroy(self, request, pk):
        product = Products.objects.filter(product_id=pk).first()
        product.delete()
        product_units = ProductUnits.objects.filter(product_id = pk)
        product_units = product_units.delete()
        message = "The product and the product units has been deleted succesfuly!"
        return Response({'message': message}, status = status.HTTP_200_OK)


    #Validation of the product units sold for the product stock, if a product unit is sold, the stock of the product will be updated
    #This validation will be executed every 30 seconds
    @scheduler.scheduled_job('interval', seconds=30)
    def validationUnitsSelledForProductStock():
        products = Products.objects.all()
        for product in products:
            product_units = ProductUnits.objects.filter(product_id = product.product_id)
            product_units_available = product_units.filter(product_unit_state = "A")
            product_units_available = product_units_available.count()
            product.stock = product_units_available
            product.save()

    scheduler.start()



    
    
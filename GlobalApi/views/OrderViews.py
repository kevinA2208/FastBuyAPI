from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Order
from GlobalApi.serializers.OrdersSerializer import OrderSerializer, ListOrderSerializer
from datetime import date
from GlobalApi.authentication.authentication_mixins import Authentication

class OrderViewSet(Authentication, viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    def get_queryset(self, id=None):
        if id == None:
            return Order.objects.all()
        return Order.objects.get(id=id)

    def create(self, request):
        date_today = date.today()
        request_data_copy = request.data.copy()
        request_data_copy['order_date'] = date_today
        serializer = self.serializer_class(data=request_data_copy)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Order created succesfuly!'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        order = Order.objects.filter(order_id = pk).first()
        serializer = self.serializer_class(order, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Order updated succesfuly!'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        order = Order.objects.filter(order_id = pk).first()
        order.delete()
        return Response({'message':'Order deleted succesfuly!'}, status= status.HTTP_200_OK)
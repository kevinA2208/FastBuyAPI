from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import Categories
from GlobalApi.serializers.CategoriesSerializer import CategoriesSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriesSerializer
    def get_queryset(self, id=None):
        if id == None:
            return Categories.objects.all()
        return Categories.objects.get(id=id)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Category created succesfuly!'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        category = Categories.objects.filter(id_category = pk).first()
        serializer = self.serializer_class(category, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'Category updated succesfuly!'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        category = Categories.objects.filter(id_category = pk).first()
        category.delete()
        return Response({'message':'Category deleted succesfuly!'}, status= status.HTTP_200_OK)


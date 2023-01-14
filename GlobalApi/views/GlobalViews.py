from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import User, Categories
from GlobalApi.serializers.CategoriesSerializer import CategoriesSerializer
from GlobalApi.serializers.UsersSerializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self, pk=None):
        if pk == None:
            return User.objects.all()
        return User.objects.get(doc=pk)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'User created succesfuly!'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #the PK is the doc, it needs to be different named
    #Cant update the pk because it creates another new object
    def update(self, request, pk=None):
        user = User.objects.filter(doc = pk).first()
        serializer = self.serializer_class(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data' : serializer.data, 'message':'User updated succesfuly!'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user = User.objects.filter(doc = pk).first()
        user.delete()
        return Response({'message':'User deleted succesfuly!'}, status= status.HTTP_200_OK)
        

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
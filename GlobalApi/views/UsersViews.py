from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework import viewsets
from GlobalApi.models import User, Client
from GlobalApi.serializers.UsersSerializer import UserSerializer, ClientSerializer, ClientInformationSerializer
from GlobalApi.authentication.authentication_mixins import Authentication


class UserViewSet(Authentication, viewsets.ModelViewSet):
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


class ClientViewSet(Authentication, viewsets.ModelViewSet):
    serializer_class = ClientInformationSerializer

    def get_queryset(self, pk=None):
        if pk == None:
            return Client.objects.all()
        return Client.objects.get(id_client=pk)

    def create(self, request):
        user_serializer = UserSerializer(data=request.data['doc_client'])

        client_data = request.data

        user_data = request.data['doc_client']
        
        user_data['user_type'] = 'C'


        if user_serializer.is_valid():
            user_doc_validated = user_serializer.validated_data['doc']
            existent_user = User.objects.filter(doc=user_doc_validated).first()
            if existent_user:
                pass
            else:
                user_serializer.save()
                
        client_data['doc_client'] = user_data['doc']

        client_serializer = ClientSerializer(data=client_data)

        if client_serializer.is_valid():
            client_doc = client_serializer.validated_data['doc_client']
            user_doc = client_doc
            existent_client = Client.objects.filter(doc_client=user_doc).first()
            if existent_client:
                return Response({'message':'Client with that document exists!'}, status= status.HTTP_400_BAD_REQUEST)
            else:
                client_serializer.save()
                return Response({'data' : client_serializer.data, 'message':'Client created succesfuly!'}, status= status.HTTP_201_CREATED)

        return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        client = Client.objects.filter(id_client = pk).first()
        
        client_data = request.data

        user_data = request.data['doc_client']

        doc_user = user_data['doc']

        user = User.objects.filter(doc = doc_user).first()

        client_data['doc_client'] = doc_user

        if doc_user != client.doc_client.doc:
            return Response({'message':'You cant change the document!'}, status= status.HTTP_400_BAD_REQUEST)
        else:
            user_serializer = UserSerializer(user, data = user_data)

            client_serializer = ClientSerializer(client, data = request.data)

            if user_serializer.is_valid():
                user_serializer.save()

            if client_serializer.is_valid():
                client_serializer.save()
                return Response({'data' : client_serializer.data, 'message':'Client updated succesfuly!'}, status= status.HTTP_201_CREATED)
        return Response(client_serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        client = Client.objects.filter(id_client = pk).first()
        user = User.objects.filter(doc = client.doc_client.doc).first()

        user.delete()
        client.delete()
        return Response({'message':'Client deleted succesfuly!'}, status= status.HTTP_200_OK)


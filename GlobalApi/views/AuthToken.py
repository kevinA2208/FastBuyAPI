from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from GlobalApi.serializers.UsersSerializer import UserTokenSerializer
from django.contrib.sessions.models import Session
from datetime import datetime
from rest_framework.views import APIView


class UserToken(APIView):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        try:
            user_token = Token.objects.get(user = UserTokenSerializer().Meta.model.objects.filter(doc=username).first())
            return Response({'token': user_token.key})
        except:
            return Response({'error': 'Wrong credentials'}, status= status.HTTP_400_BAD_REQUEST)

class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            #Bring the token, if its not created, it creates it
            token,created = Token.objects.get_or_create(user=user)
            user_serializer = UserTokenSerializer(user)
            if created:
                return Response({
                    'token': token.key,
                    'user': user_serializer.data,
                    'message': "Login succesfuly!"
                }, status = status.HTTP_201_CREATED)
            else:
                #If token exists, it deletes it and creates a new one
                token.delete()
                token = Token.objects.create(user = user)
                return Response({
                    'token': token.key,
                    'user': user_serializer.data,
                    'message': "Login succesfuly!"
                }, status = status.HTTP_201_CREATED)
                    
        else:
            return Response({'mensaje': 'Wrong document or password'}, status= status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key = token).first()
            if token:
                token.delete()
                return Response({'message': 'Token deleted succesfuly!'}, status= status.HTTP_200_OK)
            return Response({'error': 'No user found with these credentials'}, status= status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error': 'No Token found in the request'}, status= status.HTTP_409_CONFLICT)
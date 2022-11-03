from django.urls import path, include
from rest_framework.routers import DefaultRouter
from GlobalApi.views.GlobalViews import UserViewSet, ProductViewSet

router= DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]

#Tengo que revisar por que no salen los urls de la api en el servidor de prueba de la api
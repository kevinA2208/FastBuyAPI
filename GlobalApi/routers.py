from rest_framework.routers import DefaultRouter
from GlobalApi.views.GlobalViews import UserViewSet, ProductViewSet

router= DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'products', ProductViewSet, basename='products')



urlpatterns = router.urls


from rest_framework.routers import DefaultRouter
from GlobalApi.views.GlobalViews import UserViewSet
from GlobalApi.views.ProductViews import ProductViewSet
from GlobalApi.views.GlobalViews import CategoriesViewSet

router= DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', CategoriesViewSet, basename='categories')



urlpatterns = router.urls


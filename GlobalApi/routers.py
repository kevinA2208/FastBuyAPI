from rest_framework.routers import DefaultRouter
from GlobalApi.views.GlobalViews import UserViewSet, CategoriesViewSet
from GlobalApi.views.ProductViews import ProductViewSet
from GlobalApi.views.GlobalViews import ProductUnitViewSet
from GlobalApi.views.OrderViews import OrderViewSet


router= DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'productunits', ProductUnitViewSet, basename='productunits')
router.register(r'orders', OrderViewSet, basename='orders')



urlpatterns = router.urls


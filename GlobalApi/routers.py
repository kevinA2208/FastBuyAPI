from rest_framework.routers import DefaultRouter
from GlobalApi.views.GlobalViews import CategoriesViewSet
from GlobalApi.views.ProductViews import ProductViewSet, ProductUnitViewSet
from GlobalApi.views.OrderViews import OrderViewSet
from GlobalApi.views.UsersViews import ClientViewSet


router= DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'productunits', ProductUnitViewSet, basename='productunits')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'clients', ClientViewSet, basename='clients')



urlpatterns = router.urls


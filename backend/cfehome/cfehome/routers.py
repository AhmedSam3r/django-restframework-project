from rest_framework.routers import DefaultRouter

from product.viewsets import ProductViewSet, ProductGenericViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, 'products')
router.register('products-generic', ProductGenericViewSet, 'products')

urlpatterns = router.urls
# print(urlpatterns)

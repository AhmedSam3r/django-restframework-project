from rest_framework import viewsets, mixins


from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    '''
        it inherits the following:
                   mixins.CreateModelMixin,     post->create
                   mixins.RetrieveModelMixin,   get->item
                   mixins.UpdateModelMixin,     put->update
                   mixins.DestroyModelMixin,    delete->destroy
                   mixins.ListModelMixin,       get->list
                   GenericViewSet               different functions in it
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class ProductGenericViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


# A WAY to make the views more readable in sense of url(s)
# since urlpatterns of the viewsets in the routers seem ambigous
# product_list_view = ProductGenericViewSet.as_view({'get': 'list'})
# product_detail_view = ProductGenericViewSet.as_view({'get': 'retrieve'})

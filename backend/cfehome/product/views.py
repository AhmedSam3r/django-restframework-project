from rest_framework import generics, mixins, permissions
from rest_framework import authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from .models import Product
from .serializers import ProductSerializer
from api.permissions import IsStaffEdtiorPermssion
# this way the code is more maintaible instead of just writing permission all over the class
from  api.mixins import (
    StaffEditorPermissionMixin,
    UserQuerySetMixing,
)
from api.authentication import TokenAuthentication, JWTAuthentication # Moved to settings.py at rest_framework object

class ProductDetailAPIView(StaffEditorPermissionMixin,
                           generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser, IsStaffEdtiorPermssion] #as we will inherit from StaffEditorPermissionMixin no need to declare it
    lookupfield = 'pk' # Product.objects.filter(pk=1)
    
    def get_queryset(self):
        '''
            1)by overriding the super().get_queryset()
            2)writing Product.objects.filter(id=id) 
                ==> we saved up queryset time from  executing this line queryset = Product.objects.all()
                to just get one item
        '''

        id = self.kwargs.get(self.lookup_field)
        res = Product.objects.filter(id=id)
        return res

@method_decorator(require_http_methods(["OPTIONS", "GET", "POST"]), name="dispatch")
class ProductListCreateAPIView(
    UserQuerySetMixing,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):  # ListAPIView (only) (get method only)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    allow_staff_view = True
    #IsAuthenticated ==> Authentication credentials were not provided both GET and POST methods
    #IsAuthenticated ==> Authentication credentials were not provided in  POST method only, bypass get method
    # since we added the authentication classes to the SETTINGS.PY file
    # authentication_classes = [
    #     TokenAuthentication,
    #     authentication.SessionAuthentication,
    # ]
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [permissions.IsAdminUser, IsStaffEdtiorPermssion] #as we will inherit from  
    # authentication_classes = [authentication.SessionAuthentication]
    # lookupfield = 'pk' #Product.objects.get(pk=1)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content', None)
        serializer.is_valid(raise_exception=True)
        if content is None:
            content = title

        serializer.save(content=content)  # provides a default value for the content field if it's not provided in the input data.

    def ignore_get_queryset(self, *args, **kwargs):  # if we're not sure *args. **kwargs
        '''
        since we created
            class UserQuerySetMixing():
                def get_queryset(self, *args, **kwargs): return qs.filter()
            ==>in the mixin class and inherited in the view (UserQuerySetMixing)
        '''
        request = self.request
        print("@@@@@@@@@@@@@@@")
        print(request.user)
        if request.user is None:
            return Product.objects.none()
        qs = super().get_queryset(*args, **kwargs)
        print("@@@qs@@@", qs)
        return qs.filter(user=request.user)


class ProductCreateAPIView(
    UserQuerySetMixing,
    StaffEditorPermissionMixin, 
    generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookupfield = 'pk' #Product.objects.get(pk=1)
    permission_classes = [permissions.IsAdminUser, IsStaffEdtiorPermssion] #as we will inherit from  

    def perform_create(self, serializer):
        print("serializer", serializer)
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content', None)
        if content is None:
            content = title

        serializer.save(user=self.request.user, content=content) #provides a default value for the content field if it's not provided in the input data.

    def get_queryset(self, *args, **kwargs): #if we're not sure *args. **kwargs
        request = self.request
        print("@@@@@@@@@@@@@@@")
        print(request.user)
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(user=request.user)

###################################################
# Replace each class view with generic function   #
# that does the same thing combined               #
# ALL CRUD CAN BE MADE IN THE SAME VIEW           #
###################################################

@api_view(['GET', 'POST'])
def create_list_retrieve_combined(request, pk=None, *args, **kwargs):
    method = request.method

    if method == 'GET':
        ############### DETAIL VIEW ###################
        if pk is not None:
            product = get_object_or_404(Product, pk=pk)
            # queryset.exist() is False: raise Http404()
            data = ProductSerializer(product, many=False).data
            return Response(data)

        ############### LIST VIEW ###################
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data  # queryset as this is ModelSerializer class
        return Response(data)
    
    elif method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content', None)
            if content is None:
                content = title

            serializer.save(content=content)
            return Response(serializer.data)
        return Response({'message': 'invalid data'}, status=400)


from rest_framework.pagination import PageNumberPagination


class ProductMixinView(PageNumberPagination, StaffEditorPermissionMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                       mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, 
                       generics.GenericAPIView):
    '''
    SIMILAR TO create_list_retrieve_combined but it gives us more easy way to implement 
    NEED TO KNOW HOW IT WORKS
    '''

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'pk'
    # not working & can't figure it out why
    # FINALLYYY worked ===> after i added PageNumberPagination in the class declaration to inherit from 
    page_query_param = 'p'
    # permission_classes = [permissions.IsAdminUser, IsStaffEdtiorPermssion] #as we will inherit from  

    def get(self, request, *args, **kwargs):
        print("ARGS = ", args)
        print("KW", kwargs)
        pk = kwargs.get('pk')
        if pk:
            return self.retrieve(request, *args, **kwargs)
        page = super().paginate_queryset(self.queryset, request,
                                         request.resolver_match.view_name)
        if page is not None:
            context = self.get_serializer_context()
            print(super().paginator.__dict__)
            serializer = ProductSerializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    '''
    perform_create() works since mixin.CreateModelMixin()
    since in generics the createAPIView inherits both
    class CreateAPIView(StaffEditorPermissionMixin,
 mixins.CreateModelMixin,
                    GenericAPIView):

    '''

    def perform_create(self, serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content', None)
        if content is None:
            content = 'this is perform create in the mixin.CreateModelMixin'

        serializer.save(content=content) #provides a default value for the content field if it's not provided in the input data.


    def put(self, request, *args, **kwargs):
        #put is the correct word not update, update is the function
        return super().update(request, *args, **kwargs) # super() works too as we inherient the parent class instead of ((self.update()) )

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ProductUpdateAPIView(StaffEditorPermissionMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAdminUser, IsStaffEdtiorPermssion] #as we will inherit from  

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

        return Response(instance)


class ProductDeleteAPIView(StaffEditorPermissionMixin, generics.DestroyAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAdminUser, IsStaffEdtiorPermssion] #as we will inherit from  


    def get_queryset(self):
        id = self.kwargs.get(self.lookup_field)
        print("ID = ", id)
        res = Product.objects.filter(id=id) #worked when changed get to filter as it returns query set
        print("RES = ", res)
        return res

    def perform_destroy(self, instance):
        print("INSTANCE = ", instance)
        return super().perform_destroy(instance)

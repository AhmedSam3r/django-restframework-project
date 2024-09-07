from product.models import Product
from rest_framework import serializers
from rest_framework.reverse import reverse
# validate_title similar to unique
from .validators import validate_title, validate_no_hello_in_title, unique_product_title
from api.serializers import UserPublicSerializer
# from django import forms
# class ProductForum(forms.ModelForm)
#     class Meta:
#         model = Product
#         fields = [
#             'title',
#             'content',
#             'price'
#         ]

############################# PRODUCT SERIALIZER EFFECT #############################
#Title None    ===> "title":["This field may not be null."]}
#Title not exist ==>  {"title":["This field is required."]}
#price 'abc' ==> {"price":["A valid number is required."]}
###########################################################################################


class ProductInlineSerializer(serializers.Serializer):
    '''
        used to serializer a user's products in order to avoid importing product here
            ==> therefore circular import error
    '''
    title = serializers.CharField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True,
    )

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True, required=False)
    url = serializers.SerializerMethodField(read_only=True)
    # HyperlinkedIdentityField works only ModelSerializer
    # different way of constructing url
    edit_url = serializers.HyperlinkedIdentityField(
        view_name='product-update',
        lookup_field='pk'
    )
    email = serializers.EmailField(write_only=True)
    # validators useful in case of request stuff
    # BEST TO VALIDATE ON THE MODEL 
    #other way of validation
    title = serializers.CharField(validators=[unique_product_title, validate_no_hello_in_title])
    username = serializers.SerializerMethodField(read_only=True)
    owner = UserPublicSerializer(source="user", read_only=True)
    # to unify the serializers in the assumed scenarion in the course
    body = serializers.CharField(source='content') # worked 
    # without many=True i get this error: "'QuerySet' object has no attribute 'pk'"
    # why ?In summary, many=True is essential when you want to represent a queryset of related objects in your serializer, making it clear to DRF that it should handle multiple related objects, not just one.
    # related_products = ProductInlineSerializer(source="user.product_set.all",
    #                                            read_only=True, many=True)

    class Meta:
        '''
        when I added in the fields "test_best"
            django.core.exceptions.ImproperlyConfigured: Field name `test_best` is not valid for model `Product`.
        Either 
            it's a method field like my discount 
        OR
            property like sale_price in the product itself

        '''
        model = Product
        fields = [
            'owner',
            'username',
            'public',
            'email',
            'edit_url',
            'url',
            'pk',
            'title',
            # currently in the video he has shown an 'article' app similar to the product but contains body instead of content
            # what to do if we want to unify our serializers
            # let's comment for now the content
            # 'content',
            'body', #from the db model now
            'price',
            'sale_price',
            "get_discount",
            "my_discount", #what if we want to make it this way
            # "test_best",
            # "related_products",
            'path',
        ]
        extra_kwargs = {
        'title': {'required': True},  # Make 'title' field optional
        }

    # it worked too LOL, he added it in the model not here
    # ==> thats why reindexing the agolia isn't working (    raise AlgoliaIndexError(
    # algoliasearch_django.models.AlgoliaIndexError: body is not an attribute of <class 'product.models.Product'>)
    @property
    def old_get_body(self):
        '''
        I added the following in the db model
            @property
            def body(self):
                return self.content


        '''
        return self.content
    
    
    def get_username(self, obj):
        return obj.user.username
    
    #EXPLICIT it was working without explicitly declaring anything else
    def ignore_validate_title(self, title):
        queryset = Product.objects.filter(title__exact=title)
        if queryset.exists():
            raise serializers.ValidationError(f"{title} is already a product name")
        return title

    def create(self, validated_data):
        print("validated_data = ", validated_data)
        '''
        by not adding validated_data.pop('email') 
        Got a `TypeError` when calling `Product.objects.create()`. 
        This may be because you have a writable field on the serializer class that is not a valid argument to `Product.objects.create()`.
          You may need to make the field read-only, 
          or override the ProductSerializer.create() method to handle this correctly.

        '''
        email = validated_data.pop('email')
        # now you simulated an email field in the model and you can send mail to the user
        obj = super().create(validated_data)
        print('email, obj')
        print(email, obj)
        return obj

    def get_url(self, obj):
        # manualy configured url which is not practical and hard to maintain
        # return f"/api/products/{obj.pk}"
        # why not self.request ? not all the time serializers have the request ?
        # like in our manual view handling methods, passing the data without request
        request = self.context.get('request')
        if request is None:
            return ""
        return reverse("product-detail", kwargs={"pk": obj.pk}, request=request)

    def get_url(self, obj):
        # manualy configured url which is not practical and hard to maintain
        # return f"/api/products/{obj.pk}"
        # why not self.request ? not all the time serializers have the request ?
        # like in our manual view handling methods, passing the data without request
        request = self.context.get('request')
        if request is None:
            return ""
        return reverse("product-detail", kwargs={"pk": obj.pk}, request=request)

    @property
    def test_best(self):
        return "testbest"

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            print("get_my_discount==>NO ATTR ID")
            return None
        if not isinstance(obj, Product):
            print("get_my_discount==> NO INSTANCE")
            return None
        return "122"

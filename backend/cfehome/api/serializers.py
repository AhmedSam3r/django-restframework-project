from rest_framework import serializers

# class UserPublicInlineSerializer(serializers.Serializer):
#     '''
#         used to serializer a user's products in order to avoid importing product here
#             ==> therefore circular import error
#     '''
#     title = serializers.CharField(read_only=True)
#     url = serializers.HyperlinkedIdentityField(
#         view_name='product-detail',
#         lookup_field='pk',
#         read_only=True,
#     )

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    # products = serializers.SerializerMethodField(read_only=True)

    def get_products(self, obj):
        pass
        '''CONTEXT
        {
            'request': <rest_framework.request.Request: GET '/product/list-or-create/'>,
            'format': None,
            'view': <product.views.ProductListCreateAPIView object at 0x7f93fcd97c70>
        }
        '''

        # user = obj
        # user_products_qs = user.product_set.all()[0:5] 
        # self.context.get('request') very important in order to make the hyperlinkedidentity works
        # it shows us how to used nested serializer, but it's not practical in real life scenarios
        # it get all the products of the users (5 items) and display it in the inline object which isnot useful or practical
        # result = UserPublicInlineSerializer(user_products_qs, many=True,
        #                                   context=self.context)
        # return result.data
        # return []

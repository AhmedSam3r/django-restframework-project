from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Product

'''
Revisit 5:46:00 part as he suggests a challenging requirement
where you add two indexes with different models to map it in some unified way 
& how you will tackle the challenges arising from this one
'''
@register(Product)  # similar to admin.site.register(Product)
class ProductIndex(AlgoliaIndex):
    # changed to 'public' from the product model instead of 'is_public'
    should_index = 'public'
    fields = [
        'title',
        # change the content for now to body to align with the purpose of this part at course
        #unifying serializers 4:35:00
        # 'content',
        'body', # re-run the indexing command
        'price',
        'user',
        'public',
        'path',
    ]
    settings = {
        'searchableAttributes': ['title', 'body'],
        'attributesForFaceting': ['user', 'public'],
    }
    tags = 'get_tags_list'  # just string

'''
you can add other indexes for the same model (not recommended)
class ProductQuickIndexBLABLA(AlgoliaIndex):

'''
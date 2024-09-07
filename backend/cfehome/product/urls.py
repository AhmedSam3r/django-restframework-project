from django.urls import path
from . import views

urlpatterns = [
    # <type:keyword_argument>
    path('<int:pk>/', views.ProductDetailAPIView.as_view(),
         name='product-detail'),  # tutorial style but i don't like it

    path('create/', views.ProductCreateAPIView.as_view(),
         name='product-create'),
    path('list-or-create/', views.ProductListCreateAPIView.as_view(),
         name='product-list'),

     #### To make a certain view works with existence or absence of pk, you make two urls like the following 
     path('combined-views/', views.create_list_retrieve_combined,
     name='combined_views_without_pk'),
     path('combined-views/<int:pk>/', views.create_list_retrieve_combined,
         name='combined_views_with_pk'),

     path('<int:pk>/delete/', views.ProductDeleteAPIView.as_view(),
         name='product_delete'), 
     path('<int:pk>/update/', views.ProductUpdateAPIView.as_view(),
     name='product-update'), 

    path('mixin-list/', views.ProductMixinView.as_view(),
         name='product_mixin_no_pk'), #get single
    path('mixin-list/<int:pk>/', views.ProductMixinView.as_view(),
            name='product_mixing_pk'), #get list / post / update / delete
    




]

from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken
from rest_framework_simplejwt.views import TokenVerifyView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns = [
    path('', views.home),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # obtain_auth_token = ObtainAuthToken.as_view()
    path('auth/', ObtainAuthToken.as_view()),

    path('product/', views.display_product),
    path('product/add/', views.add_product)
]

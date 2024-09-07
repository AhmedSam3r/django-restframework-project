from django.urls import path

from . import views

urlpatterns = [
    path('', views.SearchListView.as_view(), name='search'),
    path('old/', views.SearchListOldView.as_view(), name='old-search'),
]

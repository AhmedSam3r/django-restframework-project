from rest_framework import generics

from product.models import Product
from product.serializers import ProductSerializer
from  . import client

from rest_framework.response import Response
from distutils.util import strtobool


class SearchListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        tag = self.request.GET.get('tag')
        public = strtobool(self.request.GET.get('public', 'false'))
        user = request.user.username if request.user.is_authenticated else None
        print("TAG = ", tag)
        print("public = ", bool(public))
        if query is None:
            return Response({'success': False}, status=400)
        results = client.perform_search(query, tag=tag, user=user,
                                        public=bool(public))
        return Response(results)


class SearchListOldView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        print("IN SEARCH q= ",q)
        results = Product.objects.none()
        if query is not None:
            qs = super().get_queryset(*args, **kwargs)
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user

            results = qs.search(query, user=user)

        return results

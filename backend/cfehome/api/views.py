from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from product.models import Product
from product.serializers import ProductSerializer

import json
# Import Django's JSON encoder
from django.core.serializers.json import DjangoJSONEncoder
from decimal import Decimal

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView


class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)  # Convert Decimal to a string representation
        return super().default(obj)

@api_view(['GET'])
def home(request):
        body = request.body #request.META older versions
        data = {}
        try:
            data = json.loads(body)
        except:
            pass        
        data["params"] = dict(request.GET)
        data["headers"] = dict(request.headers)
        data["content_type"] = request.content_type
        return Response(data)


# @api_view(['GET'])
# def display_product(request):
#     product = Product.objects.all().order_by("?").first()
#     data = {}
#     data_str = ""
#     if product:
#          data = model_to_dict(product, fields=['id', 'title', 'price', 'sale_price'])
#          print("DATA = ", data)
#          data_str = json.dumps(data,cls=DecimalEncoder)
#          print(data_str)
#         #  data["id"] = product.id
#         #  data["title"] = product.title
#         #  data["price"] = product.price
#     print(type(data))
#     # return JsonResponse(data) #accepts dict as an argument
#     print(data)
#     return HttpResponse(data_str, headers={"Content-Type": "application/json"})

@api_view(['GET'])
def display_product(request):
    instance = Product.objects.all().order_by("?").first()
    data = {}
    print("INS = ", instance)
    if instance:
        data = ProductSerializer(instance).data
        print("DATA = ", data)

    return Response(data)

@api_view(['POST'])
def add_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        # instance = serializer.save()
        print("instance", serializer.data)
    else:
        print("FALSE", serializer.errors)
        return Response(serializer.errors, status=400)

    return Response(serializer.data)

# not working
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print("@@@@@@@")
        print(response)
        print("@@@@@@@")
        print("CustomTokenObtainPairViewCustomTokenObtainPairViewCustomTokenObtainPairViewQQQ") 
        # Add CORS headers to the response
        response["Access-Control-Allow-Origin"] = "http://localhost:8111"  # Specify the allowed origin
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"  # Specify the allowed HTTP methods
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"  # Specify the allowed headers

        return Response(response)

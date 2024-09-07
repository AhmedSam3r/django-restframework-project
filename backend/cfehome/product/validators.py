from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Product


def validate_title(title):
    queryset = Product.objects.filter(title__exact=title)
    if queryset.exists():
        raise serializers.ValidationError(f"{title} is already a product name" )

    return title


def validate_no_hello_in_title(title: str):
    #i kept sepnding like 10 minutes as i was using "return" instead of raise"
    if "hello" in title.lower():
        raise serializers.ValidationError("hello is allowed in the title")

    return title

unique_product_title = UniqueValidator(queryset=Product.objects.all(), message="UniqueValidator says that's an error", lookup='iexact')
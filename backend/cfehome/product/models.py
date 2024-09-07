from django.db import models
from django.db.models import Q

from cfehome.settings import AUTH_USER_MODEL

import random

User = AUTH_USER_MODEL
TAGS_MODEL_LIST = ['electronics', 'cars', 'movies', 'goods']



class ProductQuerySet(models.QuerySet):
    def is_public(self):
        print("ProductQuerySet:::WE ARE is_public")
        return self.filter(public=True)

    def search(self, query, user=None):
        print("ProductQuerySet:::WE ARE SEARCH")
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_public().filter(lookup)
        print("ProductQuerySet:::USER ==> ", user)
        if user is not None:
            qs = qs.filter(user=user)
        return qs


class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        '''overriding the main method'''
        print("ProductManager:::WE ARE GET QUERY SET")
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        # return Product.objects.filter(public=True).filter(title__icontains=query)
        print("ProductManager:::WE ARE SEARCH")
        return self.get_queryset().filter(title__icontains=query)


class Product(models.Model):
    user = models.ForeignKey(User, default=1, null=True,
                             on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=9.99)
    public = models.BooleanField(default=True)

    objects = ProductManager()


    @property
    def path(self): #adding it in the agolia index too
        return f"/product/{self.pk}/"

    @property
    def body(self):
        return self.content

    def __str__(self) -> str:
        return self.title

    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)

    def get_discount(self):
        return "122"

    def is_public(self) -> bool:
        return self.is_public
    
    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_LIST)]

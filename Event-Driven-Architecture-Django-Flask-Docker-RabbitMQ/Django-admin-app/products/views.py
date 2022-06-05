from django.shortcuts import render

from .producer import publish
from .serializers import ProductSerializer
from .models import Product, User
import random

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class ProductViewSet(viewsets.ViewSet):
    def list(self, request): #/api/products
        products = Product.objects.all()
        serializer = ProductSerializer(instance=products, many=True)
        publish("product_fetched", {"key":"value"})
        return Response(serializer.data)
        

    def create(self, request): #/api/products
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk=None):  #/api/products/<str:id>
        my_product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(instance=my_product)
        return Response(serializer.data)

    def update(self, request, pk=None):  #/api/products/<str:id>
        my_product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(instance=my_product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



    def destroy(self, request, pk=None):  #/api/products/<str:id>
        my_product = get_object_or_404(Product, id=pk)
        my_product.delete()
        publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })
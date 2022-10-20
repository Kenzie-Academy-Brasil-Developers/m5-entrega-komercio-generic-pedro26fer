from users.serializer import UserSerializer
from rest_framework import serializers
from .models import Product


class ProductGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = ["description", "price", "quantity", "is_active", "seller"]


class ProductDetailSerializer(serializers.ModelSerializer):

    seller = UserSerializer(read_only=True)

    class Meta:
        model = Product

        fields = '__all__'

        depth = 1

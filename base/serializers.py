from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product

# serializer that wraps around the Product model, turn it into Json format
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
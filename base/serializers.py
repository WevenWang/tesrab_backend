from dataclasses import fields
from nis import cat
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem, Review, ShippingAddress


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


# serializer that wraps around the Product model, turn it into Json format
class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

# only use orderSerializer in view and nest other in orderSerializer
class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
    # when got the order, make queries for child and parent elements
    # return as nested objects
    def get_orderItems(self,obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data
    
    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False).data
        except:
            address = False
        return address
    
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data


# serializer that wraps around the User model, turn it into Json format
class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name','isAdmin']

    def get__id(self, obj):
        return obj.id

    

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name

        
# first register, new token for new user, refresh token
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name','isAdmin', 'token']
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)